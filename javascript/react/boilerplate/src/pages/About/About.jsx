import React from 'react';
import styles from './About.module.css';

const About = () => {
  return (
    <div className={styles.about}>
      <h1 className={styles.title}>About</h1>
      <p className={styles.content}>
        This is the About page. You can add more information about your
        application here.
      </p>
    </div>
  );
};

export default About;

