default:
	find . -name "*.java" -print | grep -v '/codeviz/' | xargs ../java/bin/javac -cp .:javax.json-1.0.jar:../java/lib/tools.jar 

clean:
	find . -name "*.class" -print | xargs rm
