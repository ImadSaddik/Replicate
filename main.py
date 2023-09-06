import replicate

from dotenv import load_dotenv
load_dotenv()

print((open("./bicycle.jpg", "rb")))


output = replicate.run(
    "jagilley/controlnet-scribble:435061a1b5a4c1e26740464bf786efdfa9cb3a3ac488595a2de23e143fdb0117",
    input={
        "image": open("./bicycle.jpg", "rb"),
        "prompt":"a bicycle in the snow",
        "num_samples":"1",
        "image_resolution":"512",
    }
)
print(output)
