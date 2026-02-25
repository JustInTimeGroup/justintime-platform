def extract_request_meta(request):
    """
    Collect tracking metadata safely.
    Reverse proxy ready (Phase 13 will harden this).
    """
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded:
        ip = x_forwarded.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")

    return {
        "ip_address": ip,
        "user_agent": request.META.get("HTTP_USER_AGENT", "")[:1000],
        "source_path": request.path,
    }