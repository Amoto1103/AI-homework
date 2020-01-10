P=[-1 -1 2 2 4;0 5 0 5 7];
T=[-1 -1 1 1 -1];
net=newff(P,T,5,{'tansig','purelin'},'trainrp');
net.trainParam.show=50;
net.trainParam.lr=0.05;
net.trainParam.epochs=300;
net.trainParam.goal=1e-5;
[net,tr]=train(net,P,T);

W1=net.iw{1,1};
B1=net.b{1};
W2=net.lw{2,1};

X=sim(net,P);
plot(X,'b');
hold on;
plot(T,'*');