try:
    import webview
except ImportError:
    exit('install the pywebview package')

webview.create_window('Untapped', url='./untapped.html')
webview.start(debug=False)