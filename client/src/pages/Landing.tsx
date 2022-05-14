import React, { useEffect, useState } from 'react';
import './styles/Landing.css';
import Sketch from "react-p5";
import { useNavigate } from "react-router-dom";

const Landing = () => {
  // let [width, setWidth] = useState(window.innerWidth - 20);
  // let [height, setHeight] = useState(window.innerHeight - 20);
  let width = window.innerWidth - 20;
  let height = window.innerHeight - 20;
  let navigate = useNavigate()

  let particles: Particle[] = [];
  class Particle {
    x: number;
    y: number;
    r: number;
    dx: number;
    dy: number;

    constructor(p5: any) {
      this.x = p5.random(0,width);
      this.y = p5.random(0,height);
      this.r = p5.random(3,8);
      this.dx = p5.random(-1,1);
      this.dy = p5.random(-0.5, 0.75);
    }

    render(p5: any) {
      p5.noStroke();
      p5.fill('rgba(200,169,169,0.5)');
      p5.circle(this.x,this.y,this.r);
    }

    move() {
      if(this.x < 0 || this.x > width) this.dx*=-1;
      if(this.y < 0 || this.y > height) this.dy*=-1;
      this.x+=this.dx;
      this.y+=this.dy;
    }

    connect(p5: any, particles: any) {
      particles.forEach((element: Particle) =>{
        let dis = p5.dist(this.x,this.y,element.x,element.y);
        if(dis<85) {
          p5.stroke('rgba(255,255,255,0.04)');
          p5.line(this.x,this.y,element.x,element.y);
        }
      });
    }
  }

  const setup = (p5: any, canvasParentRef: any) => {
    p5.createCanvas(window.innerWidth - 20, window.innerHeight - 20).parent(canvasParentRef);
    for(let i = 0;i<width/10;i++){
      particles.push(new Particle(p5));
    }
  }

  const draw = (p5: any) => {
    p5.background("#282c34");
      for(let i = 0;i<particles.length;i++) {
        particles[i].render(p5);
        particles[i].move();
        particles[i].connect(p5, particles.slice(i));
      }
  }

  const windowResized = (p5: any) => {
    p5.resizeCanvas(window.innerWidth-20, window.innerHeight-20);
    // setWidth(window.innerWidth-20);
    // setHeight(window.innerHeight-20);
    width = window.innerWidth-20;
    height = window.innerHeight-20;
  }

  return (
    <div className="Landing">
      <Sketch setup={setup} draw={draw} windowResized={windowResized}/>

      <div className="title-card">
        <h1>Quantum Messenger</h1>
        <p> A messaging application that uses quantum computers for end-to-end encryption!</p>
        <button onClick={() => navigate("/home")}>Get Started!</button>
      </div>
    </div>
  );
}

export default Landing;
