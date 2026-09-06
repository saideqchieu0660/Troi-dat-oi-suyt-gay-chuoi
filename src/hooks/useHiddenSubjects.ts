import { useState, useEffect } from 'react';
import { db } from '../lib/firebase';
import { doc, onSnapshot, setDoc } from 'firebase/firestore';

export function useHiddenSubjects() {
  const [hiddenSubjects, setHiddenSubjects] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onSnapshot(doc(db, 'system_config', 'library_settings'), (docSnap) => {
      if (docSnap.exists()) {
        const data = docSnap.data();
        if (data && Array.isArray(data.hiddenSubjects)) {
          setHiddenSubjects(data.hiddenSubjects);
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
      const newHidden = hiddenSubjects.includes(subject)
        ? hiddenSubjects.filter((s) => s !== subject)
        : [...hiddenSubjects, subject];
      
      // Optimistic update
      setHiddenSubjects(newHidden);

      await setDoc(doc(db, 'system_config', 'library_settings'), { 
        hiddenSubjects: newHidden, 
        updatedAt: new Date().toISOString() 
      }, { merge: true });
    } catch (e) {
      console.error("Failed to update hidden subjects", e);
      // Revert optimistic update by triggering a re-fetch (handled by snapshot)
      throw e;
    }
  };

  return { hiddenSubjects, toggleHiddenSubject, isLoading };
}
