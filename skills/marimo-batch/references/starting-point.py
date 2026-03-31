# /// script
# dependencies = [
#     "marimo",
#     "pydantic==2.12.5",
#     "python-dotenv==1.2.1",
#     "rich==14.3.2",
#     "wigglystuff==0.2.30",
#     "torch==2.11.0",
#     "wandb==0.25.1",
# ]
# requires-python = ">=3.14"
# ///

import marimo

__generated_with = "0.21.1"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""
    ## Notebook Description
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Environment Keys
    """)
    return


@app.cell
def _():
    import marimo as mo
    from dotenv import load_dotenv

    load_dotenv(".env")
    return (mo,)


@app.cell
def _(env_config, is_script_mode, wandb):
    env_config if not is_script_mode and not wandb.login() else None
    return


@app.cell
def _(ModelParams, mo, wandb):
    from wigglystuff import EnvConfig
    import sys

    is_script_mode = mo.app_meta().mode == "script"

    env_config = mo.ui.anywidget(
        EnvConfig(
            {
                "WANDB_API_KEY": lambda k: wandb.login(key=k, verify=True),
            }
        )
    )

    if is_script_mode and not mo.cli_args():
        from rich.console import Console
        from rich.table import Table

        table = Table(title="CLI Options")
        table.add_column("Flag", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Default", style="yellow")
        table.add_column("Description")

        for name, field in ModelParams.model_fields.items():
            flag = f"--{name.replace('_', '-')}"
            type_name = (
                field.annotation.__name__
                if hasattr(field.annotation, "__name__")
                else str(field.annotation)
            )
            table.add_row(flag, type_name, str(field.default), field.description or "")

        Console().print(table)
        sys.exit(0)
    return env_config, is_script_mode


@app.cell
def _():
    import wandb

    return (wandb,)


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""
    ## Training Parameters
    """)
    return


@app.cell
def _(params_form):
    params_form
    return


@app.cell
def _():
    import hashlib
    import json
    from pydantic import computed_field, BaseModel, Field


    class ModelParams(BaseModel):
        epochs: int = Field(default=25, description="Number of training epochs.")
        batch_size: int = Field(default=32, description="Training batch size.")
        learning_rate: float = Field(default=1e-4, description="Learning rate for AdamW.")
        wandb_project: str = Field(
            default="batch-sizes", description="W&B project name (empty to skip)."
        )

        @computed_field
        @property
        def run_name(self) -> str:
            parts = [
                f"e{self.epochs}",
                f"bs{self.batch_size}",
                f"lr{self.learning_rate:.0e}",
            ]
            params_dict = {
                "epochs": self.epochs,
                "batch_size": self.batch_size,
                "learning_rate": self.learning_rate,
            }
            h = hashlib.md5(json.dumps(params_dict, sort_keys=True).encode()).hexdigest()[:6]
            return "-".join(parts) + f"-{h}"

    return (ModelParams,)


@app.cell
def _(mo):
    params_form = (
        mo.md("""
    ## Model parameters

    {epochs}
    {batch_size}
    {learning_rate}
    """)
        .batch(
            epochs=mo.ui.slider(10, 50, value=50, step=1, label="epochs"),
            batch_size=mo.ui.slider(8, 512, value=32, step=8, label="batch size"),
            learning_rate=mo.ui.slider(1e-5, 5e-4, value=1e-4, step=1e-5, label="learning rate"),
        )
        .form()
    )
    return (params_form,)


@app.cell
def _(ModelParams, is_script_mode, mo, params_form):
    mo.stop(
        not is_script_mode and params_form.value is None,
        mo.md("*Submit the form to start training.*"),
    )

    if is_script_mode:
        model_params = ModelParams(**{k.replace("-", "_"): v for k, v in mo.cli_args().items()})
    else:
        model_params = ModelParams(**params_form.value)
    return (model_params,)


@app.cell
def _():
    import torch
    import torch.nn as nn

    return nn, torch


@app.cell(column=2, hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Setup
    """)
    return


@app.cell
def _(model_params, torch):
    X = torch.randn(1000, 10)
    w_true = torch.randn(10, 1)
    y = X @ w_true + 0.1 * torch.randn(1000, 1)

    dataset = torch.utils.data.TensorDataset(X, y)
    train_loader = torch.utils.data.DataLoader(
        dataset, batch_size=model_params.batch_size, shuffle=True
    )
    return (train_loader,)


@app.cell(column=3, hide_code=True)
def _(mo):
    mo.md(r"""
    ## Model Setup
    """)
    return


@app.cell
def _(nn):
    model = nn.Sequential(
        nn.Linear(10, 32),
        nn.ReLU(),
        nn.Linear(32, 1),
    )

    model
    return (model,)


@app.cell(column=4, hide_code=True)
def _(mo):
    mo.md(r"""
    ## Training Loop
    """)
    return


@app.cell
def _(mo, model, model_params, nn, torch, train_loader, wandb):
    if model_params.wandb_project:
        wandb.init(
            project=model_params.wandb_project,
            name=model_params.run_name,
            config=model_params.model_dump(),
        )

    optimizer = torch.optim.AdamW(model.parameters(), lr=model_params.learning_rate)
    loss_fn = nn.MSELoss()

    with mo.status.progress_bar(total=model_params.epochs) as bar:
        for epoch in range(model_params.epochs):
            epoch_loss = 0.0
            for xb, yb in train_loader:
                pred = model(xb)
                loss = loss_fn(pred, yb)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            avg_loss = epoch_loss / len(train_loader)
            if model_params.wandb_project:
                wandb.log({"epoch": epoch, "loss": avg_loss})
            bar.update()

    if model_params.wandb_project:
        wandb.finish()

    mo.md(f"**Training complete.** Final loss: `{avg_loss:.6f}`")
    return


if __name__ == "__main__":
    app.run()
