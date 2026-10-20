lesson "checkpoint_rollback" {
    dataset "data/iris.csv"
    test
    checkpoint "baseline"
    add_examples {
        [6.7, 3.1, 5.6, 2.4] -> "virginica"
    }
    test
    rollback "baseline"
    test
}