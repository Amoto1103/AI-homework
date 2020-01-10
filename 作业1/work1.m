clear;
P=[1 1 0 0;1 0 1 0];
T=[0 1 1 0];
net1=newff(minmax(P),[1 1],{'tansig','purelin'},'traingd');
net1.trainParam.epochs=10000;
net1.trainParam.lr=0.05;
net1=train(net1,P,T);
Y=sim(net1,P);
view(net1);
celldisp(net1.iw);
celldisp(net1.lw);
celldisp(net1.b);

plot(Y,'b');
hold on;
plot(T,'*');
