from victor import args, app_context, VictorCommand


args = args.parse_args()

app = VictorCommand(app_context)
app.from_path(args.module)
app.run()
