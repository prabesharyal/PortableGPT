message_history = {456:[{"role": "system", 123 : "hello", "content": "You are a helpful assistant"}]}
new = {"role": "system", "content": "hi"}
message_history[456].append(new)
print(message_history)
var = 123
if var in message_history:
    print("hi")