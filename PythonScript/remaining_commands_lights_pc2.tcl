python3.10 main_traffic_lights_pc2.py --epochs 50 --agents 5 --batch-size 128 --results-file lights --attack --attack-type ConstantOutput --num-exp 100 --output-dir PC2_LIGHTS_CONSTANT_STOP  --attack-strength 1 --seed 123213123
python3.10 main_traffic_lights_pc2.py --epochs 50 --agents 5 --batch-size 128 --results-file lights --attack --attack-type ConstantOutput --num-exp 100 --output-dir PC2_LIGHTS_CONSTANT_STOP_DETECT  --attack-strength 1 --seed 123213123 --allow-detection

