from .routes.jobs_simple import jobs_bp

def register_jobs_routes(app):
    """Register jobs routes with Flask app"""
    app.register_blueprint(jobs_bp)
    return app

__all__ = ['register_jobs_routes']
