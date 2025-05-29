from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

iris = load_iris(as_frame=True)
X_iris = iris.data[["petal length (cm)", "petal width (cm)"]].values
y_iris = iris.target

tree_clf=DecisionTreeClassifier(max_depth=2, random_state=42)
tree_clf.fit(X_iris, y_iris)
# Visualizing the decision tree
from sklearn.tree import export_graphviz

export_graphviz(
    tree_clf,
    out_file="iris_tree.dot",
    feature_names=["petal length(cm)","petal width(cm)"],
    class_names=iris.target_names,
    rounded=True,
    filled=True
)

from graphviz import Source

Source.from_file("iris_tree.dot")

# Predicting with the decision tree
print(tree_clf.predict_proba([[5,1.5]]).round(3))
tree_clf.predict([[5,1.5]])


from sklearn.datasets import make_moons

X_moons, y_moons = make_moons(n_samples=150,noise=0.2,random_state=42)
tree_clf1 = DecisionTreeClassifier(random_state=42)
tree_clf2 = DecisionTreeClassifier(min_samples_leaf=5, random_state=42)
tree_clf1.fit(X_moons, y_moons)
tree_clf2.fit(X_moons, y_moons)

# Visualizing the decision boundaries
# unregularized model is overfitting, and the regularized model is probably generalize better.
X_moons_test, y_moons_test = make_moons(n_samples=1000, noise=0.2, random_state=43)
tree_clf1.score(X_moons_test, y_moons_test)
tree_clf2.score(X_moons_test, y_moons_test)

#Regression tree
import numpy as np
from sklearn.tree import DecisionTreeRegressor

np.random.seed(2)
X_quad = np.random.rand(200, 1) - 0.5 #a single random input feature
y_quad = X_quad**2 + 0.025*np.random.randn(200, 1) #quadratic function with some noise
tree_reg = DecisionTreeRegressor(max_depth=2, random_state=42)
tree_reg.fit(X_quad, y_quad)