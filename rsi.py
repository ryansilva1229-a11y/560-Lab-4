# This script is used in sma_rsi.py to compute rsi

def calculate_avg_gain(prices):
    gains = []
    for i in range(1, len(prices)):
        gain = prices[i] - prices[i - 1]
        if gain > 0:
            gains.append(gain)
        else:
            gains.append(0)
    avg_gain = sum(gains) / len(gains) if gains else 0
    return avg_gain

def calculate_avg_loss(prices):
    losses = []
    for i in range(1, len(prices)):
        loss = prices[i - 1] - prices[i]
        if loss > 0:
            losses.append(loss)
        else:
            losses.append(0)
    avg_loss = sum(losses) / len(losses) if losses else 0
    return avg_loss

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    avg_gain = calculate_avg_gain(prices[-(period + 1):])
    avg_loss = calculate_avg_loss(prices[-(period + 1):])

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi