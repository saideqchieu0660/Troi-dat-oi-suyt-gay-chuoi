import os

with open("src/lib/PomodoroStore.ts", "r") as f:
    content = f.read()

# We need to add the recordPomodoroSession method to the class
import_statements = "import { auth, db } from './firebase';\nimport { doc, setDoc } from 'firebase/firestore';\n"
content = import_statements + content

record_func = """
  private recordPomodoroSession(elapsedSeconds: number) {
    if (elapsedSeconds < 60) return; // Skip if less than 1 min
    try {
      const minutes = Math.floor(elapsedSeconds / 60);
      const today = new Date().toISOString().split('T')[0];
      
      const statsStr = localStorage.getItem('vibe_pomodoro_stats');
      let stats = statsStr ? JSON.parse(statsStr) : {};
      if (!stats[today]) stats[today] = { count: 0, timeSpent: 0 };
      stats[today].count += 1;
      stats[today].timeSpent += minutes;
      localStorage.setItem('vibe_pomodoro_stats', JSON.stringify(stats));

      const histStr = localStorage.getItem('vibe_pomodoro_history');
      let history = histStr ? JSON.parse(histStr) : [];
      history.push({
        id: Date.now().toString(),
        duration: minutes,
        timestamp: Date.now(),
        dateStr: new Date().toLocaleDateString('vi-VN'),
        deckTitle: "Phiên Pomodoro"
      });
      if (history.length > 50) history = history.slice(history.length - 50);
      localStorage.setItem('vibe_pomodoro_history', JSON.stringify(history));

      window.dispatchEvent(new Event('vibe_pomodoro_updated'));

      // Safe Cloud Sync - fire and forget
      if (auth && auth.currentUser) {
        setDoc(doc(db, "users", auth.currentUser.uid, "vibe_metrics", "pomodoro"), {
          stats,
          history,
          lastUpdatedAt: Date.now()
        }, { merge: true }).catch(err => console.error(err));
      }
    } catch (err) {
      console.error("Failed to save Pomodoro session stats:", err);
    }
  }
"""

content = content.replace("class PomodoroGlobalStore {", "class PomodoroGlobalStore {" + record_func)

# Fix stop() method
content = content.replace(
    """  stop() {
    this.pause();
    this.updateState({
      mode: 'work',
      timeLeft: this.state.workTime,
      isBreakLocked: false
    });
  }""",
    """  stop() {
    this.pause();
    if (this.state.mode === 'work') {
      const elapsed = this.state.workTime - this.state.timeLeft;
      this.recordPomodoroSession(elapsed);
    }
    this.updateState({
      mode: 'work',
      timeLeft: this.state.workTime,
      isBreakLocked: false
    });
  }"""
)

# Fix skipBreak() method
content = content.replace(
    """  skipBreak() {
    this.updateState({
      mode: 'work',
      timeLeft: this.state.workTime,
      isActive: false,
      isBreakLocked: false
    });
    if (this.interval) clearInterval(this.interval);
    this.interval = null;
  }""",
    """  skipBreak() {
    if (this.state.mode === 'work') {
      const elapsed = this.state.workTime - this.state.timeLeft;
      this.recordPomodoroSession(elapsed);
    }
    this.updateState({
      mode: 'work',
      timeLeft: this.state.workTime,
      isActive: false,
      isBreakLocked: false
    });
    if (this.interval) clearInterval(this.interval);
    this.interval = null;
  }"""
)

# Fix tick() method
old_tick_recording = """        // --- GHI NHẬN POMODORO THÀNH CÔNG VÀO LOCALSTORAGE ---
        try {
          const statsStr = localStorage.getItem('vibe_pomodoro_stats');
          const today = new Date().toISOString().split('T')[0];
          let stats = statsStr ? JSON.parse(statsStr) : {};
          
          if (!stats[today]) stats[today] = { count: 0, timeSpent: 0 };
          stats[today].count += 1;
          // Tính thời gian dựa trên workTime
          stats[today].timeSpent += Math.floor(this.state.workTime / 60);
          
          localStorage.setItem('vibe_pomodoro_stats', JSON.stringify(stats));
          window.dispatchEvent(new Event('vibe_pomodoro_updated'));
        } catch (err) {
          console.error("Failed to save Pomodoro session stats:", err);
        }"""

new_tick_recording = """        // --- GHI NHẬN POMODORO THÀNH CÔNG VÀO LOCALSTORAGE VÀ CLOUD ---
        this.recordPomodoroSession(this.state.workTime);"""

content = content.replace(old_tick_recording, new_tick_recording)

with open("src/lib/PomodoroStore.ts", "w") as f:
    f.write(content)
