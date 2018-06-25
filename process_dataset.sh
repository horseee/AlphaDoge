#/bin/bash
mkdir ./train
for file in ./CGOS9x9/*.bz2
do 
    echo $file
    tar xvjf $file  -C ./train
done

echo "Merging dataset..."
python3 merge_dataset.py