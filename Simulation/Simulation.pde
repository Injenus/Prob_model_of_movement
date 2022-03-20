import controlP5.*; //<>//
ControlP5 cp5;

PImage img;
PFont font;

float REAL_DATA[][][];
float PREDICT_DATA[][][];
byte REAL_POSITION[][];
byte PREDICT_POSITION[][];


int NUM;
String MAP;
int pHeight;
int pWidth;
float origin[]={52.5, 170.5, 52.5+665.1, 170.5};

boolean move=false;
int step=0;
boolean finish=false;
int fps;
int ratio;

float currentValue;
boolean isReset=false;
boolean manually=false;

void setup() {
  size(1298, 660);
  noStroke();
  cp5 = new ControlP5(this);
  font=createFont("arial bold italic", 16);

  cp5.addButton("Start")
    .setPosition(10, 10)
    .setSize(100, 50)
    .setFont(font);
  cp5.addButton("Stop")
    .setPosition(10+110, 10)
    .setSize(100, 50)
    .setFont(font);
  cp5.addButton("Reset")
    .setPosition(10+2*110, 10)
    .setSize(100, 50)
    .setFont(font);
  cp5.addSlider("Progress")
    .setPosition(399, 10)
    .setSize(500, 50)
    .setRange(0, 100)
    .setNumberOfTickMarks(NUM)
    .setLabel("Progress (%)")
    .setFont(font);
    cp5.addButton("Reload")
      .setPosition(1298-10-100, 10)
      .setSize(100, 50)
      .setFont(font);

  NUM=int(loadStrings("data.csv")[0]);
  MAP=loadStrings("data.csv")[1];
  pHeight=int(loadStrings("data.csv")[2]);
  pWidth=int(loadStrings("data.csv")[3]);
  fps=int(loadStrings("data.csv")[4]);  // more than 16 is ineffective //<>// //<>// //<>// //<>//
  ratio=int(loadStrings("data.csv")[5]);;  // int(fr/ratio) = speed (cells per second)
  frameRate(fps);
  REAL_DATA=new float[NUM][pHeight][pWidth];
  PREDICT_DATA=new float[NUM][pHeight][pWidth];
  REAL_POSITION=new byte[NUM][2];
  PREDICT_POSITION=new byte[NUM][2];
  getData(REAL_DATA, "real_data.csv");
  getData(PREDICT_DATA, "predict_data.csv");
  getPosition(REAL_POSITION, "real_pos.csv");
  getPosition(PREDICT_POSITION, "predict_pos.csv");
  delay(10);
}

void draw() {
  img = loadImage(MAP);
  background(img);
  cp5.get(Slider.class, "Progress").showTickMarks(true);

  cp5.get(Slider.class, "Progress").getCaptionLabel().setColor(color(0));

  currentValue=cp5.get(Slider.class, "Progress").getValue();
  //println(cp5.get(Slider.class, "Progress").getValue());

  if (!manually) {
    if (step>1) {
      //print("STEP > 1: ");
      //println(step);
      //if (abs(currentValue-float((step-2)/ratio)*100/(NUM-1))<2*100/(NUM-1)) {
      if (abs(currentValue-float((step-2)/ratio)*100/(NUM-1))<1.49*100/(NUM)) {

        if (finish) {
          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawRealRobot(i, j, REAL_DATA[NUM-1][i][j], false);
            }
          }
          drawRealRobot(REAL_POSITION[NUM-1][0], REAL_POSITION[NUM-1][1], 0, true);

          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawPredictRobot(i, j, PREDICT_DATA[NUM-1][i][j], false);
            }
          }
          drawPredictRobot(PREDICT_POSITION[NUM-1][0], PREDICT_POSITION[NUM-1][1], 0, true);

          cp5.get(Slider.class, "Progress").setValue(100);
        } else {
          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawRealRobot(i, j, REAL_DATA[int(step/ratio)][i][j], false);
            }
          }
          drawRealRobot(REAL_POSITION[int(step/ratio)][0], REAL_POSITION[int(step/ratio)][1], 0, true);

          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawPredictRobot(i, j, PREDICT_DATA[int(step/ratio)][i][j], false);
            }
          }
          drawPredictRobot(PREDICT_POSITION[int(step/ratio)][0], PREDICT_POSITION[int(step/ratio)][1], 0, true);

          if (int(step/ratio)==0) {
            cp5.get(Slider.class, "Progress").setValue(int(0));
          } else { //<>//
            cp5.get(Slider.class, "Progress").setValue(float(step/ratio)*100/(NUM-1));
          }
        }
      } else {
        inf();
      }
    } else {   //if step<=1
      if (currentValue==0) {
        if (finish) { //<>//
          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawRealRobot(i, j, REAL_DATA[NUM-1][i][j], false);
            }
          }
          drawRealRobot(REAL_POSITION[NUM-1][0], REAL_POSITION[NUM-1][1], 0, true);

          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawPredictRobot(i, j, PREDICT_DATA[NUM-1][i][j], false);
            }
          }
          drawPredictRobot(PREDICT_POSITION[NUM-1][0], PREDICT_POSITION[NUM-1][1], 0, true);

          cp5.get(Slider.class, "Progress").setValue(100);
        } else {
          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawRealRobot(i, j, REAL_DATA[int(step/ratio)][i][j], false);
            }
          }
          drawRealRobot(REAL_POSITION[int(step/ratio)][0], REAL_POSITION[int(step/ratio)][1], 0, true);

          for (int i=0; i<pHeight; i++) {
            for (int j=0; j<pWidth; j++) {
              drawPredictRobot(i, j, PREDICT_DATA[int(step/ratio)][i][j], false);
            }
          }
          drawPredictRobot(PREDICT_POSITION[int(step/ratio)][0], PREDICT_POSITION[int(step/ratio)][1], 0, true);

          if (int(step/ratio)==0) {
            cp5.get(Slider.class, "Progress").setValue(int(0));
          } else {
            cp5.get(Slider.class, "Progress").setValue(float(step/ratio)*100/(NUM-1));
          }
        }
      } else {
        inf();
      }
    }  // конец если не ручное
  } else {
    inf();
  }

  if (move)step++;
  if ((int(step/ratio))==NUM) {
    move=false;
    step=0; 
    isReset=false;
    finish=true;
  }
}

void getPosition(byte ARR[][], String name) {
  String[] textLines = loadStrings(name);
  for (int i=0; i<NUM; i++) {
    String[] coord = split(textLines[i], ",");
    for (int j=0; j<2; j++) {
      ARR[i][j]=byte(int(coord[j]));
    }
  }
  //println();
  //for (int i=0; i<NUM; i++) {
  //  for (int j=0; j<2; j++) {
  //    print(ARR[i][j]);
  //  }
  //  println();
  //}
}

void getData(float ARR[][][], String name) {
  String[] textLines = loadStrings(name);
  //print("All data: ");
  //println(textLines);
  //println();

  for (int i=0; i<NUM; i++) {
    for (int j = 0; j < pHeight; j++ ) {
      String[] elOfRow = split(textLines[j+pHeight*i], ",");      
      //print("Stroka ");
      //print(i, j);
      //print(": ");
      //println(elOfRow);     
      for (int el = 0; el < elOfRow.length; el++) {
        ARR[i][j%8][el]=float(elOfRow[el]);
      }
    }
  }
  //println();
  //for (int i=0; i<NUM; i++) {
  //  for (int j=0; j<pHeight; j++) {
  //    for (int k=0; k<pWidth; k++) {
  //      print(ARR[i][j][k]);
  //      print(" ");
  //    }
  //    println();
  //  }
  //  println("#");
  //}
}

void drawRealRobot(float y, float x, float alpha, boolean main) {
  float dy=0.37*x;
  float dx=0.1*y;
  alpha=alpha*255;
  if (y%2==0) {
    fill(0, alpha);
    circle(x*70.33+origin[0]+dx, y*61.55+origin[1]+dy, 54);
    if (main) {
      fill(128, 166, 255, 240);
      circle(x*70.33+origin[0]+dx, y*61.55+origin[1]+dy, 18);
    }
  } else {
    fill(0, alpha);
    circle(x*70.33+origin[0]+70.33/2-0.09+dx, y*61.55+origin[1]+dy, 54);
    if (main) {
      fill(128, 166, 255, 240);
      circle(x*70.33+origin[0]+70.33/2-0.09+dx, y*61.55+origin[1]+dy, 18);
    }
  }
}

void drawPredictRobot(float y, float x, float alpha, boolean main) {
  float dy=0.42*x;
  float dx=0.09*y;
  //alpha=(alpha+0.1)*255*(1+(alpha));
  //alpha=(sqrt(alpha))*255;
  //alpha=(log(alpha+1.15))*255*1.1;
  //alpha=(sqrt(log(alpha+1)*1.6))*255;
  alpha=0.66*(sqrt(log(alpha+1.005)*2.4))*255;
  if (y%2==0) {
    fill(0, alpha);
    circle(x*70.33+origin[2]+dx, y*61.55+origin[3]+dy, 54);
    if (main) {
      fill(128, 166, 255, 240);
      circle(x*70.33+origin[2]+dx, y*61.55+origin[3]+dy, 18);
    }
  } else {
    fill(0, alpha);
    circle(x*70.33+origin[2]+70.33/2-0.09+dx, y*61.55+origin[3]+dy, 54);
    if (main) {
      fill(128, 166, 255, 240);
      circle(x*70.33+origin[2]+70.33/2-0.09+dx, y*61.55+origin[3]+dy, 18);
    }
  }
}

void Start() {
  move=true;
  manually=false;
}

void Stop() {
  move=false;
}

void Reset() {
  move=false;
  finish=false;
  isReset=true;
  manually=false;
  step=0;
}

void inf() {
  manually=true;
  move=false;
  finish=false;
  if (isReset) {
    step=0; 
    isReset=false;
  } else step=int(ratio*currentValue*(NUM-1)/100);  
  //print("STEP INF  ");
  //print(step);
  //print(":  :");
  //print(currentValue);
  //print(":  ;");
  //println(step/ratio);

  for (int i=0; i<pHeight; i++) {
    for (int j=0; j<pWidth; j++) {
      drawRealRobot(i, j, REAL_DATA[int(step/ratio)][i][j], false);
    }
  }
  drawRealRobot(REAL_POSITION[int(step/ratio)][0], REAL_POSITION[int(step/ratio)][1], 0, true);

  for (int i=0; i<pHeight; i++) {
    for (int j=0; j<pWidth; j++) {
      drawPredictRobot(i, j, PREDICT_DATA[int(step/ratio)][i][j], false);
    }
  }
  drawPredictRobot(PREDICT_POSITION[int(step/ratio)][0], PREDICT_POSITION[int(step/ratio)][1], 0, true);

  if (int(step/ratio)==0) {
    cp5.get(Slider.class, "Progress").setValue(int(0));
  } else {
    cp5.get(Slider.class, "Progress").setValue(float(step/ratio)*100/(NUM-1));
  }
  redraw();
}
void Reload(){
  setup();
}
