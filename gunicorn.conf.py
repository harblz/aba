bind = "0.0.0.0:8000"
accesslog = "./access.log"
def ssl_context(conf, default_ssl_context_factory):
    import ssl
    context = default_ssl_context_factory()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    return context