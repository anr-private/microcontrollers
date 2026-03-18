class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [0] * size
        self.count = 0
        self.peak = 0  # <--- Track the maximum ever reached

    def put(self, val):
        if self.count == self.size: return False
        # ... (rest of put logic)
        self.count += 1
        if self.count > self.peak:
            self.peak = self.count # Update peak
        return True

###

