lesson "multi_checkpoints" {
    dataset "data/iris.csv"
    checkpoint "start"
    test
    add_examples {
        [5.0, 3.4, 1.5, 0.2] -> "setosa"
        [6.3, 2.5, 5.0, 1.9] -> "virginica"
    }
    checkpoint "after_add"
    test
    rollback "start"
    test
    rollback "after_add"
    test
}