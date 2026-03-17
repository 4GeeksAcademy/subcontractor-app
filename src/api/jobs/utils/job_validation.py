from datetime import datetime

def validate_job_data(data, is_update=False):
    """Validate job data"""
    errors = {}
    
    # Title validation
    if not is_update or 'title' in data:
        title = data.get('title', '').strip()
        if not title:
            errors['title'] = 'Title is required'
        elif len(title) < 3:
            errors['title'] = 'Title must be at least 3 characters'
        elif len(title) > 100:
            errors['title'] = 'Title must be less than 100 characters'
    
    # Description validation
    if not is_update or 'description' in data:
        description = data.get('description', '').strip()
        if not description:
            errors['description'] = 'Description is required'
        elif len(description) < 10:
            errors['description'] = 'Description must be at least 10 characters'
        elif len(description) > 1000:
            errors['description'] = 'Description must be less than 1000 characters'
    
    # Location validation
    if not is_update or 'location' in data:
        location = data.get('location', '').strip()
        if not location:
            errors['location'] = 'Location is required'
        elif len(location) < 5:
            errors['location'] = 'Location must be at least 5 characters'
        elif len(location) > 200:
            errors['location'] = 'Location must be less than 200 characters'
    
    # Budget validation
    if not is_update or 'budget' in data:
        budget = data.get('budget')
        if budget is None or budget == '':
            errors['budget'] = 'Budget is required'
        else:
            try:
                budget_float = float(budget)
                if budget_float <= 0:
                    errors['budget'] = 'Budget must be greater than 0'
                elif budget_float > 1000000:
                    errors['budget'] = 'Budget must be less than $1,000,000'
            except (ValueError, TypeError):
                errors['budget'] = 'Budget must be a valid number'
    
    # Start date validation
    if not is_update or 'startDate' in data:
        start_date = data.get('startDate')
        if not start_date:
            errors['startDate'] = 'Start date is required'
        else:
            try:
                start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                today = datetime.utcnow().date()
                if start_date_obj.date() < today:
                    errors['startDate'] = 'Start date cannot be in the past'
            except (ValueError, TypeError):
                errors['startDate'] = 'Start date must be a valid date'
    
    # End date validation
    if not is_update or 'endDate' in data:
        end_date = data.get('endDate')
        if end_date:
            try:
                end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                
                # Check if end date is after start date
                start_date = data.get('startDate')
                if start_date:
                    try:
                        start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                        if end_date_obj <= start_date_obj:
                            errors['endDate'] = 'End date must be after start date'
                    except (ValueError, TypeError):
                        errors['endDate'] = 'Invalid start date format'
            except (ValueError, TypeError):
                errors['endDate'] = 'End date must be a valid date'
    
    # Priority validation
    if not is_update or 'priority' in data:
        priority = data.get('priority', 'medium')
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if priority not in valid_priorities:
            errors['priority'] = 'Priority must be one of: ' + ', '.join(valid_priorities)
    
    # Status validation
    if not is_update or 'status' in data:
        status = data.get('status', 'pending')
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled', 'on_hold']
        if status not in valid_statuses:
            errors['status'] = 'Status must be one of: ' + ', '.join(valid_statuses)
    
    # Categories validation
    if not is_update or 'categories' in data:
        categories = data.get('categories', [])
        if categories and not isinstance(categories, list):
            errors['categories'] = 'Categories must be a list'
        elif categories:
            valid_categories = [
                'residential', 'commercial', 'industrial', 'renovation',
                'new_construction', 'remodeling', 'plumbing', 'electrical',
                'hvac', 'roofing', 'painting', 'flooring', 'landscaping',
                'concrete', 'carpentry'
            ]
            invalid_categories = [cat for cat in categories if cat not in valid_categories]
            if invalid_categories:
                errors['categories'] = f'Invalid categories: {", ".join(invalid_categories)}'
    
    # Customer ID validation
    if not is_update or 'customerId' in data:
        customer_id = data.get('customerId')
        if not customer_id:
            errors['customerId'] = 'Customer is required'
        else:
            try:
                customer_id_int = int(customer_id)
                if customer_id_int <= 0:
                    errors['customerId'] = 'Customer ID must be a positive integer'
            except (ValueError, TypeError):
                errors['customerId'] = 'Customer ID must be a valid number'
    
    # Progress validation
    if not is_update or 'progress' in data:
        progress = data.get('progress')
        if progress is not None:
            try:
                progress_int = int(progress)
                if progress_int < 0 or progress_int > 100:
                    errors['progress'] = 'Progress must be between 0 and 100'
            except (ValueError, TypeError):
                errors['progress'] = 'Progress must be a valid number'
    
    return errors

def validate_job_status_change(current_status, new_status):
    """Validate if status change is allowed"""
    valid_transitions = {
        'pending': ['in_progress', 'cancelled'],
        'in_progress': ['completed', 'cancelled', 'on_hold'],
        'on_hold': ['in_progress', 'cancelled'],
        'completed': [],  # Terminal state
        'cancelled': []   # Terminal state
    }
    
    if new_status not in valid_transitions.get(current_status, []):
        return False, f'Cannot change status from {current_status} to {new_status}'
    
    return True, None

def validate_file_upload(file):
    """Validate uploaded file"""
    errors = {}
    
    if not file:
        errors['file'] = 'No file provided'
        return errors
    
    if file.filename == '':
        errors['file'] = 'No file selected'
        return errors
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if hasattr(file, 'content_length') and file.content_length > max_size:
        errors['file'] = 'File size must be less than 10MB'
    
    # Check file extension
    allowed_extensions = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'gif'}
    if '.' not in file.filename:
        errors['file'] = 'File must have an extension'
    else:
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in allowed_extensions:
            errors['file'] = f'File type .{extension} is not allowed'
    
    return errors

def validate_worker_assignment(data):
    """Validate worker assignment data"""
    errors = {}
    
    # Worker ID validation
    worker_id = data.get('workerId')
    if not worker_id:
        errors['workerId'] = 'Worker ID is required'
    else:
        try:
            worker_id_int = int(worker_id)
            if worker_id_int <= 0:
                errors['workerId'] = 'Worker ID must be a positive integer'
        except (ValueError, TypeError):
            errors['workerId'] = 'Worker ID must be a valid number'
    
    # Role validation
    role = data.get('role', 'Worker')
    if not role or len(role.strip()) == 0:
        errors['role'] = 'Role is required'
    elif len(role) > 100:
        errors['role'] = 'Role must be less than 100 characters'
    
    return errors

def sanitize_search_query(query):
    """Sanitize search query"""
    if not query:
        return ''
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$', '(', ')']
    sanitized = query
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Limit length
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    return sanitized

def validate_pagination_params(page, per_page):
    """Validate pagination parameters"""
    errors = {}
    
    # Page validation
    if page is None:
        page = 1
    else:
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            errors['page'] = 'Page must be a valid number'
    
    # Per page validation
    if per_page is None:
        per_page = 20
    else:
        try:
            per_page = int(per_page)
            if per_page < 1:
                per_page = 20
            elif per_page > 100:
                per_page = 100
        except (ValueError, TypeError):
            errors['per_page'] = 'Per page must be a valid number between 1 and 100'
    
    return page, per_page, errors
