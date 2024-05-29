import React, { useEffect, useState } from 'react';
import { getDatabase, ref, onValue } from "firebase/database";
import { database } from './firebaseConfig';

const RealtimeDataComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const dbRef = ref(database, 'path/to/your/data');
    const unsubscribe = onValue(dbRef, (snapshot) => {
      const data = snapshot.val();
      setData(data);
    });

    // クリーンアップ関数を返す
    return () => unsubscribe();
  }, []);

  return (
    <div>
      <h1>Realtime Data</h1>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default RealtimeDataComponent;
