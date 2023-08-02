clear all
close all
clc

%% Parametric run
epochs = 1:25;


%Without Detection
constantOutputAttackFile = 'ConstantOutputAttack.json'; % filename in JSON extension 
constantOutputAttackDataP = fileread(constantOutputAttackFile); % dedicated for reading files as text 
constantOutputAttackData = jsondecode(constantOutputAttackDataP); % Using the jsondecode function to parse JSON from string 

for i = 1 : length(epochs) 
    currentTarget = sprintf("Epoch%dTarget",i);
    currentPred = sprintf("Epoch%dPred",i);
    
    disp(constantOutputAttackData.('currentTarget'))
    
end


%% Constant Output Attack

epochs = 1:10;
%With Detection
constantOutputAttackFile = 'ConstantOutputAttackWithDetection.json'; % filename in JSON extension 
constantOutputAttackDataP = fileread(constantOutputAttackFile); % dedicated for reading files as text 
constantOutputAttackData = jsondecode(constantOutputAttackDataP); % Using the jsondecode function to parse JSON from string 

%Parse Data:
Epoch1Target = constantOutputAttackData.Epoch1Target;
Epoch1Pred = constantOutputAttackData.Epoch1Pred;
Epoch2Target = constantOutputAttackData.Epoch2Target;
Epoch2Pred = constantOutputAttackData.Epoch2Pred;
Epoch3Target = constantOutputAttackData.Epoch3Target;
Epoch3Pred = constantOutputAttackData.Epoch3Pred;
Epoch4Target = constantOutputAttackData.Epoch4Target;
Epoch4Pred = constantOutputAttackData.Epoch4Pred;
Epoch5Target = constantOutputAttackData.Epoch5Target;
Epoch5Pred = constantOutputAttackData.Epoch5Pred;
Epoch6Target = constantOutputAttackData.Epoch6Target;
Epoch6Pred = constantOutputAttackData.Epoch6Pred;
Epoch7Target = constantOutputAttackData.Epoch7Target;
Epoch7Pred = constantOutputAttackData.Epoch7Pred;
Epoch8Target = constantOutputAttackData.Epoch8Target;
Epoch8Pred = constantOutputAttackData.Epoch8Pred;
Epoch9Target = constantOutputAttackData.Epoch9Target;
Epoch9Pred = constantOutputAttackData.Epoch9Pred;
Epoch10Target = constantOutputAttackData.Epoch10Target;
Epoch10Pred = constantOutputAttackData.Epoch10Pred;

resultDetection = zeros(10,1);

resultDetection(1) = sum(Epoch1Pred(:) == Epoch1Target(:)) / length(Epoch1Pred(:));
resultDetection(2) = sum(Epoch2Pred(:) == Epoch2Target(:)) / length(Epoch2Pred(:));
resultDetection(3) = sum(Epoch3Pred(:) == Epoch3Target(:)) / length(Epoch3Pred(:));
resultDetection(4) = sum(Epoch4Pred(:) == Epoch4Target(:)) / length(Epoch4Pred(:));
resultDetection(5) = sum(Epoch5Pred(:) == Epoch5Target(:)) / length(Epoch5Pred(:));
resultDetection(6) = sum(Epoch6Pred(:) == Epoch6Target(:)) / length(Epoch6Pred(:));
resultDetection(7) = sum(Epoch7Pred(:) == Epoch7Target(:)) / length(Epoch7Pred(:));
resultDetection(8) = sum(Epoch8Pred(:) == Epoch8Target(:)) / length(Epoch8Pred(:));
resultDetection(9) = sum(Epoch9Pred(:) == Epoch9Target(:)) / length(Epoch9Pred(:));
resultDetection(10) = sum(Epoch10Pred(:) == Epoch10Target(:)) / length(Epoch10Pred(:));

%Without Detection
constantOutputAttackFile = 'ConstantOutputAttack.json'; % filename in JSON extension 
constantOutputAttackDataP = fileread(constantOutputAttackFile); % dedicated for reading files as text 
constantOutputAttackData = jsondecode(constantOutputAttackDataP); % Using the jsondecode function to parse JSON from string 

%Parse Data:
Epoch1Target = constantOutputAttackData.Epoch1Target;
Epoch1Pred = constantOutputAttackData.Epoch1Pred;
Epoch2Target = constantOutputAttackData.Epoch2Target;
Epoch2Pred = constantOutputAttackData.Epoch2Pred;
Epoch3Target = constantOutputAttackData.Epoch3Target;
Epoch3Pred = constantOutputAttackData.Epoch3Pred;
Epoch4Target = constantOutputAttackData.Epoch4Target;
Epoch4Pred = constantOutputAttackData.Epoch4Pred;
Epoch5Target = constantOutputAttackData.Epoch5Target;
Epoch5Pred = constantOutputAttackData.Epoch5Pred;
Epoch6Target = constantOutputAttackData.Epoch6Target;
Epoch6Pred = constantOutputAttackData.Epoch6Pred;
Epoch7Target = constantOutputAttackData.Epoch7Target;
Epoch7Pred = constantOutputAttackData.Epoch7Pred;
Epoch8Target = constantOutputAttackData.Epoch8Target;
Epoch8Pred = constantOutputAttackData.Epoch8Pred;
Epoch9Target = constantOutputAttackData.Epoch9Target;
Epoch9Pred = constantOutputAttackData.Epoch9Pred;
Epoch10Target = constantOutputAttackData.Epoch10Target;
Epoch10Pred = constantOutputAttackData.Epoch10Pred;

resultAttack = zeros(10,1);

resultAttack(1) = sum(Epoch1Pred(:) == Epoch1Target(:)) / length(Epoch1Pred(:));
resultAttack(2) = sum(Epoch2Pred(:) == Epoch2Target(:)) / length(Epoch2Pred(:));
resultAttack(3) = sum(Epoch3Pred(:) == Epoch3Target(:)) / length(Epoch3Pred(:));
resultAttack(4) = sum(Epoch4Pred(:) == Epoch4Target(:)) / length(Epoch4Pred(:));
resultAttack(5) = sum(Epoch5Pred(:) == Epoch5Target(:)) / length(Epoch5Pred(:));
resultAttack(6) = sum(Epoch6Pred(:) == Epoch6Target(:)) / length(Epoch6Pred(:));
resultAttack(7) = sum(Epoch7Pred(:) == Epoch7Target(:)) / length(Epoch7Pred(:));
resultAttack(8) = sum(Epoch8Pred(:) == Epoch8Target(:)) / length(Epoch8Pred(:));
resultAttack(9) = sum(Epoch9Pred(:) == Epoch9Target(:)) / length(Epoch9Pred(:));
resultAttack(10) = sum(Epoch10Pred(:) == Epoch10Target(:)) / length(Epoch10Pred(:));

attackTarget = 0;

successfullAttack = zeros(10,1);
successfullAttack(1) = 0;sum(Epoch1Pred(:) == attackTarget) / length(Epoch1Pred(:));
successfullAttack(2) = 0;sum(Epoch2Pred(:) == attackTarget) / length(Epoch2Pred(:));
successfullAttack(3) = 0;sum(Epoch3Pred(:) == attackTarget) / length(Epoch3Pred(:));
successfullAttack(4) = sum(Epoch4Pred(:) == attackTarget) / length(Epoch4Pred(:));
successfullAttack(5) = sum(Epoch5Pred(:) == attackTarget) / length(Epoch5Pred(:));
successfullAttack(6) = sum(Epoch6Pred(:) == attackTarget) / length(Epoch6Pred(:));
successfullAttack(7) = sum(Epoch7Pred(:) == attackTarget) / length(Epoch7Pred(:));
successfullAttack(8) = sum(Epoch8Pred(:) == attackTarget) / length(Epoch8Pred(:));
successfullAttack(9) = sum(Epoch9Pred(:) == attackTarget) / length(Epoch9Pred(:));
successfullAttack(10) = sum(Epoch10Pred(:) == attackTarget) / length(Epoch10Pred(:));


%Print
figure;
subplot(2,1,1);
hold on
plot(epochs,resultAttack,'--','LineWidth',2);
plot(epochs,resultDetection,'LineWidth',2);
plot([3,3],[0,1],'k','LineWidth',2)
l = legend("Constant Label Attack", "Detection");
set(l,'FontSize',10);
set(l,'Location','SouthWest');
xlabel("Epochs",'FontSize',15);
title("Constant Label Attack - Probability of true classification",'FontSize',15);
subplot(2,1,2);
plot(epochs,successfullAttack,'--','LineWidth',2);
xlabel("Epochs",'FontSize',15);
title("Constant Label Attack - Probability of succesfully attack",'FontSize',15);
hold on
plot([3,3],[0,1],'k','LineWidth',2)


%% Label Flip Attack

epochs = 1:10;
%With Detection
constantOutputAttackFile = 'LabelFlipAttackWithDetection.json'; % filename in JSON extension 
constantOutputAttackDataP = fileread(constantOutputAttackFile); % dedicated for reading files as text 
constantOutputAttackData = jsondecode(constantOutputAttackDataP); % Using the jsondecode function to parse JSON from string 

%Parse Data:
Epoch1Target = constantOutputAttackData.Epoch1Target;
Epoch1Pred = constantOutputAttackData.Epoch1Pred;
Epoch2Target = constantOutputAttackData.Epoch2Target;
Epoch2Pred = constantOutputAttackData.Epoch2Pred;
Epoch3Target = constantOutputAttackData.Epoch3Target;
Epoch3Pred = constantOutputAttackData.Epoch3Pred;
Epoch4Target = constantOutputAttackData.Epoch4Target;
Epoch4Pred = constantOutputAttackData.Epoch4Pred;
Epoch5Target = constantOutputAttackData.Epoch5Target;
Epoch5Pred = constantOutputAttackData.Epoch5Pred;
Epoch6Target = constantOutputAttackData.Epoch6Target;
Epoch6Pred = constantOutputAttackData.Epoch6Pred;
Epoch7Target = constantOutputAttackData.Epoch7Target;
Epoch7Pred = constantOutputAttackData.Epoch7Pred;
Epoch8Target = constantOutputAttackData.Epoch8Target;
Epoch8Pred = constantOutputAttackData.Epoch8Pred;
Epoch9Target = constantOutputAttackData.Epoch9Target;
Epoch9Pred = constantOutputAttackData.Epoch9Pred;
Epoch10Target = constantOutputAttackData.Epoch10Target;
Epoch10Pred = constantOutputAttackData.Epoch10Pred;

resultDetection = zeros(10,1);

resultDetection(1) = sum(Epoch1Pred(:) == Epoch1Target(:)) / length(Epoch1Pred(:));
resultDetection(2) = sum(Epoch2Pred(:) == Epoch2Target(:)) / length(Epoch2Pred(:));
resultDetection(3) = sum(Epoch3Pred(:) == Epoch3Target(:)) / length(Epoch3Pred(:));
resultDetection(4) = sum(Epoch4Pred(:) == Epoch4Target(:)) / length(Epoch4Pred(:));
resultDetection(5) = sum(Epoch5Pred(:) == Epoch5Target(:)) / length(Epoch5Pred(:));
resultDetection(6) = sum(Epoch6Pred(:) == Epoch6Target(:)) / length(Epoch6Pred(:));
resultDetection(7) = sum(Epoch7Pred(:) == Epoch7Target(:)) / length(Epoch7Pred(:));
resultDetection(8) = sum(Epoch8Pred(:) == Epoch8Target(:)) / length(Epoch8Pred(:));
resultDetection(9) = sum(Epoch9Pred(:) == Epoch9Target(:)) / length(Epoch9Pred(:));
resultDetection(10) = sum(Epoch10Pred(:) == Epoch10Target(:)) / length(Epoch10Pred(:));

%Without Detection
constantOutputAttackFile = 'LabelFlipAttack.json'; % filename in JSON extension 
constantOutputAttackDataP = fileread(constantOutputAttackFile); % dedicated for reading files as text 
constantOutputAttackData = jsondecode(constantOutputAttackDataP); % Using the jsondecode function to parse JSON from string 

%Parse Data:
Epoch1Target = constantOutputAttackData.Epoch1Target;
Epoch1Pred = constantOutputAttackData.Epoch1Pred;
Epoch2Target = constantOutputAttackData.Epoch2Target;
Epoch2Pred = constantOutputAttackData.Epoch2Pred;
Epoch3Target = constantOutputAttackData.Epoch3Target;
Epoch3Pred = constantOutputAttackData.Epoch3Pred;
Epoch4Target = constantOutputAttackData.Epoch4Target;
Epoch4Pred = constantOutputAttackData.Epoch4Pred;
Epoch5Target = constantOutputAttackData.Epoch5Target;
Epoch5Pred = constantOutputAttackData.Epoch5Pred;
Epoch6Target = constantOutputAttackData.Epoch6Target;
Epoch6Pred = constantOutputAttackData.Epoch6Pred;
Epoch7Target = constantOutputAttackData.Epoch7Target;
Epoch7Pred = constantOutputAttackData.Epoch7Pred;
Epoch8Target = constantOutputAttackData.Epoch8Target;
Epoch8Pred = constantOutputAttackData.Epoch8Pred;
Epoch9Target = constantOutputAttackData.Epoch9Target;
Epoch9Pred = constantOutputAttackData.Epoch9Pred;
Epoch10Target = constantOutputAttackData.Epoch10Target;
Epoch10Pred = constantOutputAttackData.Epoch10Pred;

resultAttack = zeros(10,1);

resultAttack(1) = sum(Epoch1Pred(:) == Epoch1Target(:)) / length(Epoch1Pred(:));
resultAttack(2) = sum(Epoch2Pred(:) == Epoch2Target(:)) / length(Epoch2Pred(:));
resultAttack(3) = sum(Epoch3Pred(:) == Epoch3Target(:)) / length(Epoch3Pred(:));
resultAttack(4) = sum(Epoch4Pred(:) == Epoch4Target(:)) / length(Epoch4Pred(:));
resultAttack(5) = sum(Epoch5Pred(:) == Epoch5Target(:)) / length(Epoch5Pred(:));
resultAttack(6) = sum(Epoch6Pred(:) == Epoch6Target(:)) / length(Epoch6Pred(:));
resultAttack(7) = sum(Epoch7Pred(:) == Epoch7Target(:)) / length(Epoch7Pred(:));
resultAttack(8) = sum(Epoch8Pred(:) == Epoch8Target(:)) / length(Epoch8Pred(:));
resultAttack(9) = sum(Epoch9Pred(:) == Epoch9Target(:)) / length(Epoch9Pred(:));
resultAttack(10) = sum(Epoch10Pred(:) == Epoch10Target(:)) / length(Epoch10Pred(:));

attackTarget = 0;

successfullAttack = zeros(10,1);
successfullAttack(1) = 0;sum(Epoch1Pred(:) == attackTarget) / length(Epoch1Pred(:));
successfullAttack(2) = 0;sum(Epoch2Pred(:) == attackTarget) / length(Epoch2Pred(:));
successfullAttack(3) = 0;sum(Epoch3Pred(:) == attackTarget) / length(Epoch3Pred(:));
successfullAttack(4) = sum(Epoch4Pred(:) == attackTarget) / length(Epoch4Pred(:));
successfullAttack(5) = sum(Epoch5Pred(:) == attackTarget) / length(Epoch5Pred(:));
successfullAttack(6) = sum(Epoch6Pred(:) == attackTarget) / length(Epoch6Pred(:));
successfullAttack(7) = sum(Epoch7Pred(:) == attackTarget) / length(Epoch7Pred(:));
successfullAttack(8) = sum(Epoch8Pred(:) == attackTarget) / length(Epoch8Pred(:));
successfullAttack(9) = sum(Epoch9Pred(:) == attackTarget) / length(Epoch9Pred(:));
successfullAttack(10) = sum(Epoch10Pred(:) == attackTarget) / length(Epoch10Pred(:));


%Print
figure;
subplot(2,1,1);
hold on
plot(epochs,resultAttack,'--','LineWidth',2);
plot(epochs,resultDetection,'LineWidth',2);
plot([3,3],[0,1],'k','LineWidth',2)
l = legend("Label Flip Attack", "Detection");
set(l,'FontSize',10);
set(l,'Location','SouthWest');
xlabel("Epochs",'FontSize',15);
title("Label Flip Attack - Probability of true classification",'FontSize',15);
subplot(2,1,2);
plot(epochs,successfullAttack,'--','LineWidth',2);
xlabel("Epochs",'FontSize',15);
title("Label Flip Attack - Probability of succesfully attack",'FontSize',15);
hold on
plot([3,3],[0,1],'k','LineWidth',2)



%%


%Without Detection
constantOutputAttackFile = 'ConstantOutputAttack.json'; % filename in JSON extension 
constantOutputAttackDataP = fileread(constantOutputAttackFile); % dedicated for reading files as text 
constantOutputAttackData = jsondecode(constantOutputAttackDataP); % Using the jsondecode function to parse JSON from string 
%Without Detection
LabelFlipAttackFile = 'LabelFlipAttack.json'; % filename in JSON extension 
LabelFlipAttackDataP = fileread(LabelFlipAttackFile); % dedicated for reading files as text 
LabelFlipAttackData = jsondecode(LabelFlipAttackDataP); % Using the jsondecode function to parse JSON from string 


sum(constantOutputAttackData.Epoch9Pred(:) == LabelFlipAttackData.Epoch9Pred(:))
