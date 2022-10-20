from fastapi import FastAPI

import OpenDebates

# Create App Instance
app = FastAPI(title="Open Debates", version=OpenDebates.__version__)
