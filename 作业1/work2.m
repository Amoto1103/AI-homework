clear;
P=[1 1 0 0;1 0 1 0];
T=[0 1 1 0];
net2=newff(minmax(P),[2 1],{'tansig','purelin'},'traingd');
net2.trainParam.epochs=10000;
net2.trainParam.lr=0.05;
net2=train(net2,P,T);
Y=sim(net2,P);
view(net2);
celldisp(net2.iw);
celldisp(net2.lw);
celldisp(net2.b);

plot(Y,'b');
hold on;
plot(T,'*');