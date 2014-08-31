from victor import args, Victor


args = args.parse_args()

app = Victor()
app.from_path(args.module)
app.run()
