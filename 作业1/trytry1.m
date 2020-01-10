clear;
P=[1 1 0 0;1 0 1 0];
T=[0 1 1 0];
net=newrbe(P,T);
view(net);
y=sim(net,P);