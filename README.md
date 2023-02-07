# Lightning Serve

Lightning Serve is a simple and highly customizable framework to orchestrate most ML serving frameworks on [lightning.ai](https://lightning.ai/).

## API

The `Lightning Serve` library exposes `ServeFlow` and several strategies such as `BlueGreenStrategy`, `RecreateStrategy`, etc...

```py
from lightning import LightningFlow, LightningApp
from lightning_serve import ServeFlow
from datetime import datetime

class RootFlow(LightningFlow):

    def __init__(self):
        super().__init__()

        self.serve = ServeFlow(
            strategy="ramped",
            script_path="./scripts/serve.py",
        )

    def run(self):
        # Deploy a new server every time the provided input changes
        # and shutdown the previous server once the new one is ready.
        self.serve.run(random_kwargs=datetime.now().strftime("%m/%d/%Y, %H:%M"))

    def configure_layout(self):
        return {"name": "Serve", "content": self.serve.url + "/predict"}

app = LightningApp(RootFlow(), debug=True)
```

### Currently Supported Strategy

Inspired from [Kubernetes deployment strategies](https://github.com/ContainerSolutions/k8s-deployment-strategies)

- [x] recreate: terminate the old version and release the new one
- [x] ramped: release a new version on a rolling update fashion, one after the other
- [x] blue/green: release a new version alongside the old version then switch traffic
- \[\] canary: release a new version to a subset of users, then proceed to a full rollout
- [x] a/b testing: release a new version to a subset of users in a precise way
  - \[\] (HTTP headers)
  - \[\] cookie
  - [x] weighted
- [x] shadow: release a new version alongside the old version. Incoming traffic is mirrored to the new version and doesn't impact the response.

### Coming Soon

- \[\] Batching Inference
- \[\] Save, Load for any models (Tensorflow, Keras, PyTorch, PyTorch Lightning).
- \[\] Auto Scale / Load Balancing
- \[\] Sharded Inference
- \[\] Native Optimized Kubernetes
- \[\] Monitoring (Prometheus, Grafana)
- \[\] Built-in Load Testing.
