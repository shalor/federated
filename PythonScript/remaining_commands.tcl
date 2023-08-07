mkdir -p ConstantOutputAttackNoDelay
python3.9 main.py --epochs 100 --agents 10 --batch-size 128 --results-file Attack10AgentsNoDelay --attack --attack-type ConstantOutput
exec mv Attack10AgentsNoDelay.json ConstantOutputAttackNoDelay/
echo "HERE: Finished 10 Agents - Trustworthy"

