import React from 'react';
import Button from '../../components/common/Button/Button';
import styles from './Home.module.css';

const Home = () => {
  const handleClick = () => {
    alert('Button clicked!');
  };

  return (
    <div className={styles.home}>
      <h1 className={styles.title}>Welcome to React App</h1>
      <p className={styles.description}>
        This is a boilerplate React application following best practices and
        design patterns.
      </p>
      <Button onClick={handleClick} variant="primary">
        Get Started
      </Button>
    </div>
  );
};

export default Home;

