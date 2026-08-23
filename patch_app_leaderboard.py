import sys

with open("src/App.tsx", "r") as f:
    content = f.read()

import_statement = "import { useLeaderboard } from './hooks/useLeaderboard';\n"
if "import { useLeaderboard }" not in content:
    content = content.replace("import { useEffect", import_statement + "import { useEffect")

old_use_effect = """  useEffect(() => {
    if (!user) {
      setCurrentUserRank(null);
      return;
    }
    let unsub = () => {};
    const setupRankingListener = async () => {
      try {
        const { db } = await import("./lib/firebase");
        const { collection, getDocs, query, where, limit } = await import("firebase/firestore");
        const usersCol = collection(db, "users");
        
        // SỬA LỖI FULL TABLE SCAN GÂY CẠN QUOTA READS
        // Lazy Boot: limit to 10 to save reads during Vibe Coding
        const q = query(usersCol, where("points", ">", 0), limit(10));
        const snapshot = await getDocs(q);
        const usersList: any[] = [];
        snapshot.forEach((doc) => {
          usersList.push({ id: doc.id, ...doc.data() });
        });
        const sorted = usersList.sort(
          (a, b) => (b.points || 0) - (a.points || 0),
        );
        const index = sorted.findIndex((u: any) => u.id === user.uid);
        if (index !== -1) {
          setCurrentUserRank(index + 1);
        } else {
          setCurrentUserRank(null);
        }
      } catch (e) {
        console.error(
          "Error setting up ranking fetch inside App.tsx:",
          e,
        );
      }
    };
    setupRankingListener();
    return () => {};
  }, [user?.uid]);"""

new_use_effect = """  const { data: leaderboardData } = useLeaderboard(!!user?.uid);
  useEffect(() => {
    if (leaderboardData && user?.uid) {
      const sorted = leaderboardData.sort(
        (a: any, b: any) => (b.points || 0) - (a.points || 0),
      );
      const index = sorted.findIndex((u: any) => u.id === user.uid);
      if (index !== -1) {
        setCurrentUserRank(index + 1);
      } else {
        setCurrentUserRank(null);
      }
    } else {
      setCurrentUserRank(null);
    }
  }, [leaderboardData, user?.uid]);"""

content = content.replace(old_use_effect, new_use_effect)

with open("src/App.tsx", "w") as f:
    f.write(content)
