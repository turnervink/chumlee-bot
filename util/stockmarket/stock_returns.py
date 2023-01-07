def get_portfolio_time_weighted_return(portfolio: dict, current_stock_price: int):
    current_portfolio_value = portfolio["stockQty"] * current_stock_price

    if current_portfolio_value == 0:
        return 0

    history = portfolio["history"]
    history.sort(key=lambda x: x["timestamp"])

    time_period_returns = []
    for transaction in history:
        period_start_value = transaction["startValue"]
        period_end_value = transaction["endValue"]
        cash_flow = transaction["qty"] * transaction["price"] * (1 if transaction["action"] == "buy" else -1)
        period_return = (period_end_value - (period_start_value + cash_flow)) / (period_start_value + cash_flow)
        time_period_returns.append(period_return)

        print(period_return)

    final_period_return = (current_portfolio_value - (history[-1]["endValue"] + 0)) / (current_portfolio_value + 0)
    print(final_period_return)
    time_period_returns.append(final_period_return)

    twr = 0
    for period_return in time_period_returns:
        twr = twr * (1 + period_return)

    print(twr - 1)
    return twr


if __name__ == "__main__":
    get_portfolio_time_weighted_return({
        "stockQty": 50,
        "history": [
            {
                "timestamp": "2021-01-01 00:00:00",
                "action": "buy",
                "qty": 100,
                "price": 100,
                "startValue": 0,
                "endValue": 10000,
            },
            {
                "timestamp": "2021-01-02 00:00:00",
                "action": "sell",
                "qty": 50,
                "price": 200,
                "startValue": 20000,
                "endValue": 10000
            }
        ]
    }, 300)
