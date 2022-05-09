for dir in folder/*/
do
	echo $dir
	echo $dir
	cd $dir
	pwd
	cd ..
	pwd
#	7z x $dir/**.gz -o$dir
done
