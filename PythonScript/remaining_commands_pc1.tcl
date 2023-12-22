#python3.8 main.py --epochs 1000 --agents 5 --batch-size 128 --results-file MultipleUnsyncedAttackers --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced
#python3.8 main.py --epochs 300 --agents 10 --batch-size 128 --results-file MultipleUnsyncedAttackers --attack --attack-type ConstantOutput --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced --attack-strength 1
#python3.8 main.py --epochs 300 --agents 10 --batch-size 128 --results-file MultipleUnsyncedAttackers --attack --attack-type ConstantOutput --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced
python3.8 main.py --epochs 50 --agents  3 --batch-size 128 --results-file ROC --attack --attack-type ConstantOutput --num-exp 50 --output-dir NEW_PC1_ROC1_Plots_3Agents  --attack-strength 1 --seed 123213123
python3.8 main.py --epochs 50 --agents  5 --batch-size 128 --results-file ROC --attack --attack-type ConstantOutput --num-exp 50 --output-dir NEW_PC1_ROC1_Plots_5Agents  --attack-strength 1 --seed 123213123
python3.8 main.py --epochs 50 --agents 10 --batch-size 128 --results-file ROC --attack --attack-type ConstantOutput --num-exp 50 --output-dir NEW_PC1_ROC1_Plots_10Agents --attack-strength 1 --seed 123213123

