import type { NextPage } from 'next';
import { useState } from 'react';
import { createStyles, Card, Text } from '@mantine/core';

const useStyles = createStyles((theme, _params, getRef) => {
  const child = getRef('child');

  return {
    body: {
      width: "100vw",
      height: "100vh",
      backgroundColor: theme.colors.indigo[9]
    },

    card: {
      width: "30vw",
      height: "30vh",
      minHeight: "10rem",
      minWidth: "10rem",
      position: 'absolute',
      left: "35vw",
      top: "35vh",
      paddingLeft: "5rem",
      paddingRight: "5rem",
    },

    text: {
      marginTop: 0,
      marginBottom: '.5rem',
    }
  };
});

const Landing: NextPage = () => {
  const { classes } = useStyles();

  return (
    <div className={classes.body}>
      <Card shadow="sm" padding="lg" className={classes.card}>
        <Text align="center" size="xl" weight={700} className={classes.text}>Quantum Messenger</Text>
        <Text size="md">A messanging service that uses quantum computers for end-to-end encryption</Text>
      </Card>
    </div>
  );
}

export default Landing;
