This is a simple package to use topsis(technique for Order of preference by Similarity to Ideal Solution)
approach to select best among many things based on different attributes, such as selecting the best
Machine Learning algorithms based on correlation,R-square,root mean square error and accuracy.
You can use this simple package to get ranks on basis of topsis approach, ypu simply need to pass 
NumPy array after pre-processing your data along with weights between 0 and 1 and all weights should
sum to 1 to get correct results and you need to pass impacts as well in form of '+' or '-' 
where '+' indicates that you need to maximise value of that particular column and '-' indicates that
you need to minimise value of that particular column.
After passing all these parameters you will get your rank row.