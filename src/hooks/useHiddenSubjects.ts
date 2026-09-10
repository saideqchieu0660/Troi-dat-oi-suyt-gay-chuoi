import { useState, useEffect } from 'react';
import { db } from '../lib/firebase';
import { doc, onSnapshot, setDoc } from 'firebase/firestore';

export function useHiddenSubjects() {
  const [hiddenCategories, setHiddenSubjects] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onSnapshot(doc(db, 'vibe_settings', 'dashboard_config'), (docSnap) => {
      if (docSnap.exists()) {
        const data = docSnap.data();
        if (data && Array.isArray(data.hiddenCategories)) {
          setHiddenSubjects(data.hiddenCategories);
        } else {
          setHiddenSubjects([]);
        }
      } else {
        setHiddenSubjects([]);
      }
      setIsLoading(false);
    }, (error) => {
      console.warn(`[HiddenSubjects] Failed to read library settings`, error);
      setIsLoading(false);
    });
    return () => unsubscribe();
  }, []);

  const toggleHiddenSubject = async (subject: string) => {
    try {
      const newHidden = hiddenCategories.includes(subject)
        ? hiddenCategories.filter((s) => s !== subject)
        : [...hiddenCategories, subject];
      
      // Optimistic update
      setHiddenSubjects(newHidden);

      await setDoc(doc(db, 'vibe_settings', 'dashboard_config'), { 
        hiddenCategories: newHidden, 
        updatedAt: new Date().toISOString() 
      }, { merge: true });
    } catch (e) {
      console.error("Failed to update hidden subjects", e);
      // Revert optimistic update by triggering a re-fetch (handled by snapshot)
      throw e;
    }
  };

  return { hiddenCategories, toggleHiddenSubject, isLoading };
}
