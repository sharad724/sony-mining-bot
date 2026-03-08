import React, { useState, useEffect } from 'react';

function App() {
  const [userId, setUserId] = useState(null);
  const [balance, setBalance] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // URL se Telegram ID lo
    const params = new URLSearchParams(window.location.search);
    const id = params.get('userId');
    
    if (id) {
      setUserId(id);
      localStorage.setItem('telegramId', id);
      
      // Demo balance (actual Firebase se ayega)
      setTimeout(() => {
        setBalance(1250.50);
        setLoading(false);
      }, 1000);
    } else {
      setLoading(false);
    }
  }, []);

  // Style objects
  const styles = {
    container: {
      maxWidth: '800px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: '-apple-system, sans-serif'
    },
    header: {
      textAlign: 'center',
      padding: '20px',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      color: 'white',
      borderRadius: '10px',
      marginBottom: '20px'
    },
    card: {
      background: 'white',
      padding: '20px',
      borderRadius: '10px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      marginBottom: '20px'
    },
    balance: {
      fontSize: '36px',
      fontWeight: 'bold',
      margin: '10px 0'
    },
    grid: {
      display: 'grid',
      gridTemplateColumns: '1fr 1fr',
      gap: '10px'
    },
    statBox: {
      background: '#f5f5f5',
      padding: '15px',
      borderRadius: '8px',
      textAlign: 'center'
    },
    button: {
      background: '#0088cc',
      color: 'white',
      border: 'none',
      padding: '10px 20px',
      borderRadius: '5px',
      fontSize: '16px',
      cursor: 'pointer',
      textDecoration: 'none',
      display: 'inline-block'
    }
  };

  if (loading) {
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h1>⛏️ Sony Mining</h1>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!userId) {
    return (
      <div style={styles.container}>
        <div style={styles.header}>
          <h1>⛏️ Sony Mining</h1>
          <p>Please login with Telegram</p>
        </div>
        <div style={{...styles.card, textAlign: 'center'}}>
          <p>Bot se dashboard button click karo</p>
          <a 
            href="https://t.me/SON_Mining_Bot" 
            style={styles.button}
            target="_blank"
            rel="noopener noreferrer"
          >
            Open @SON_Mining_Bot
          </a>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h1>⛏️ Sony Mining</h1>
        <p>ID: {userId.substring(0, 8)}...</p>
      </div>

      {/* Balance Card */}
      <div style={styles.card}>
        <h2>Your Balance</h2>
        <div style={styles.balance}>{balance} SON</div>
        <p>Mining Rate: 0.5 SON/hour</p>
      </div>

      {/* Stats Grid */}
      <div style={styles.grid}>
        <div style={styles.statBox}>
          <h3>Total Mined</h3>
          <p style={{fontSize: '20px', fontWeight: 'bold'}}>1,250 SON</p>
        </div>
        <div style={styles.statBox}>
          <h3>Referrals</h3>
          <p style={{fontSize: '20px', fontWeight: 'bold'}}>5</p>
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{...styles.grid, marginTop: '20px'}}>
        <a 
          href={`https://t.me/SON_Mining_Bot`}
          style={{...styles.button, textAlign: 'center'}}
          target="_blank"
          rel="noopener noreferrer"
        >
          Open Bot
        </a>
        <button 
          style={{...styles.button, background: '#764ba2'}}
          onClick={() => window.location.reload()}
        >
          Refresh
        </button>
      </div>
    </div>
  );
}

export default App;
