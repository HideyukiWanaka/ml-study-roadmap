from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import make_moons
from sklearn.datasets import load_iris
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

iris = load_iris(as_frame=True)
X = iris.data[["petal length (cm)", "petal width (cm)"]].values
y = (iris.target == 2)

# Linera SVM classifier
svm_clf = make_pipeline(StandardScaler(), LinearSVC(C=1, random_state=42))
svm_clf.fit(X, y)

X_new = [[5.5, 1.7], [5.0, 1.5]]
print(svm_clf.predict(X_new))
print(svm_clf.decision_function(X_new))

# Non-linear SVM classifier
X, y = make_moons(n_samples=100, noise=0.15, random_state=42)
polynominal_svm_clf = make_pipeline(PolynomialFeatures(degree=3),
                                    StandardScaler(),
                                    LinearSVC(C=10, max_iter=10_000, random_state=42))
polynominal_svm_clf.fit(X, y)
