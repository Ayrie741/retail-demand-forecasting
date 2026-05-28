from darts.dataprocessing.transformers.reconciliation import (
    BottomUpReconciliator,
    TopDownReconciliator,
    MinTReconciliator
)


def apply_bottom_up(prediction, hierarchy):
    """
    Apply Bottom-Up reconciliation.

    This method starts from the most granular store-item forecasts
    and aggregates them upward.
    """

    reconciler = BottomUpReconciliator()

    return reconciler.transform(
        prediction.with_hierarchy(hierarchy)
    )


def apply_top_down(train, prediction, hierarchy):
    """
    Apply Top-Down reconciliation.

    This method starts from the total-level forecast and distributes
    it down to lower levels based on historical proportions.
    """

    reconciler = TopDownReconciliator()
    reconciler.fit(train.with_hierarchy(hierarchy))

    return reconciler.transform(
        prediction.with_hierarchy(hierarchy)
    )


def apply_mint(train, prediction, hierarchy, method="wls_val"):
    """
    Apply MinT reconciliation.

    MinT adjusts forecasts using an error-based reconciliation strategy.
    """

    reconciler = MinTReconciliator(method)
    reconciler.fit(train.with_hierarchy(hierarchy))

    return reconciler.transform(
        prediction.with_hierarchy(hierarchy)
    )