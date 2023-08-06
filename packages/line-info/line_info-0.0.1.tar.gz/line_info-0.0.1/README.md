# line_info

CLI tool to fetch helpful info about line of code, such as issue number, related PRs, etc.

Usage: 
```bash
line_info path/to/file line_number [selected_text]
```

It's designed to be used as an extension for IDE and called with a shortcut.

For example, in your Intellij IDE you can add this tool to `Extention Tools` (**Preferences -> Tools -> Extention Tools**)
Use `line_info` as Program and `"$FilePath$" $LineNumber$ "$SelectedText$"` as Arguments
Then you can bind any shortcut or run it from context menu


