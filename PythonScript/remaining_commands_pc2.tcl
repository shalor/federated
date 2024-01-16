#python3.8 main.py --epochs 1000 --agents 5 --batch-size 128 --results-file MultipleUnsyncedAttackers --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced
#python3.8 main.py --epochs 300 --agents 10 --batch-size 128 --results-file MultipleUnsyncedAttackers --attack --attack-type ConstantOutput --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced --attack-strength 1
#python3.8 main.py --epochs 300 --agents 10 --batch-size 128 --results-file MultipleUnsyncedAttackers --attack --attack-type ConstantOutput --num-exp 1 --output-dir PC1_MultipleAttackersNotSynced
#python3.10 main.py --epochs 30 --agents 5 --batch-size 128 --results-file NON_IID --attack --attack-type ConstantOutput --num-exp 100 --output-dir PC2_NON_IID_Detection_Plots --allow-detection --attack-strength 1 --seed 12312
#python3.10 main.py --epochs 30 --agents 6 --batch-size 128 --results-file NON_IID --attack --attack-type ConstantOutput --num-exp 100 --output-dir PC2_NON_IID_6agents_Detection_Plots --allow-detection --attack-strength 1
#python3.10 main.py --epochs 30 --agents 6 --batch-size 128 --results-file NON_IID --attack --attack-type ConstantOutput --num-exp 100 --output-dir PC2_NON_IID_6agents_Detection_NEW --allow-detection --attack-strength 1
#python3.10 main.py --epochs 50 --agents 4 --batch-size 128 --results-file NON_IID --num-exp 20 --output-dir PC2_NON_IID_4agents_Detection_NEW --attack --attack-type ConstantOutput --allow-detection --attack-strength 1
python3.10 main.py --epochs 50 --agents 6 --batch-size 128 --results-file NON_IID --num-exp 150 --output-dir PC2_NON_IID_6agents_ROC_NEW --attack --attack-type ConstantOutput --attack-strength 1
#python3.10 main.py --epochs 50 --agents 6 --batch-size 128 --results-file NON_IID --num-exp 150 --output-dir PC2_NON_IID_6agents_NO_ATTACK2

