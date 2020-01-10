clear;
P=[1 1 0 0;1 0 1 0];
T=[0 1 1 0];
net3=newff(minmax(P),[3 1],{'tansig','purelin'},'traingd');
net3.trainParam.epochs=1000;
net3.trainParam.lr=0.05;
net3=train(net3,P,T);
Y=sim(net3,P);
view(net3);
celldisp(net3.iw);
celldisp(net3.lw);
celldisp(net3.b);

plot(Y,'b');
hold on;
plot(T,'*');