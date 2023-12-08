#python3.8 main.py --epochs 1000 --agents 5 --batch-size 128 --results-file MultipleUnsyncedAttackers --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced
#python3.8 main.py --epochs 300 --agents 10 --batch-size 128 --results-file MultipleUnsyncedAttackers --attack --attack-type ConstantOutput --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced --attack-strength 1
#python3.8 main.py --epochs 300 --agents 10 --batch-size 128 --results-file MultipleUnsyncedAttackers --attack --attack-type ConstantOutput --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced
python3.8 main.py --epochs 50 --agents 5 --batch-size 128 --results-file ROC --attack --attack-type ConstantOutput --num-exp 100 --output-dir PC1_ROC1_Plots --attack-strength 1

