# from django.apps import AppConfig


# class MentorshipConfig(AppConfig):
#     name = 'mentorship'

# C:\Users\Admin\Desktop\TheYKSApp\mentorship\api.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import MentorshipSession, Booking, MentorshipVideo
import secrets

User = get_user_model()

# ======================================================================
# 🎥 MENTORSHIP VIDEOS (Mentor uploads → Students view)
# ======================================================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def video_list_api(request):
    # ── GET: List all active videos ────────────────────────────────
    if request.method == 'GET':
        videos = MentorshipVideo.objects.filter(is_active=True).select_related('mentor')
        data = [{
            'id': v.id,
            'title': v.title,
            'video_url': v.video_url,
            'description': v.description,
            'mentor_name': getattr(v.mentor, 'full_name', None) or v.mentor.email,
            'mentor_role': getattr(v.mentor, 'role', 'MENTOR'),
            'category': v.category,
            'created_at': v.created_at.isoformat(),
        } for v in videos]
        return Response({'success': True, 'videos': data})

    # ── POST: Mentor uploads video URL ─────────────────────────────
    title = request.data.get('title', '').strip()
    video_url = request.data.get('video_url', '').strip()
    
    if not title or not video_url:
        return Response({'success': False, 'error': 'Title and video URL are required.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Only MENTORS, ADMINS, SUPER_ADMINS can upload
    user_role = getattr(request.user, 'role', '')
    if user_role not in ['MENTOR', 'ADMIN', 'SUPER_ADMIN']:
        return Response({'success': False, 'error': 'Only mentors can upload videos.'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    video = MentorshipVideo.objects.create(
        mentor=request.user,
        title=title,
        video_url=video_url,
        description=request.data.get('description', ''),
        category=request.data.get('category', ''),
    )
    
    return Response({
        'success': True, 
        'message': 'Video uploaded successfully.',
        'video_id': video.id
    }, status=status.HTTP_201_CREATED)


# ======================================================================
# 📅 SESSIONS & BOOKINGS
# ======================================================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def session_list_api(request):
    # ── GET: List sessions ─────────────────────────────────────────
    if request.method == 'GET':
        sessions = MentorshipSession.objects.all().select_related('mentor', 'student')
        data = [{
            'id': s.id,
            'mentor': getattr(s.mentor, 'full_name', None) or s.mentor.email,
            'student': getattr(s.student, 'full_name', None) or s.student.email,
            'session_type': s.session_type,
            'date': str(s.date),
            'time': str(s.time),
            'status': s.status,
            'meeting_link': s.meeting_link,
        } for s in sessions]
        return Response({'success': True, 'sessions': data})

    # ── POST: Create/Book a session ────────────────────────────────
    mentor_id = request.data.get('mentor_id')
    session_type = request.data.get('session_type', 'ONE_ON_ONE')
    date = request.data.get('date')
    time = request.data.get('time')
    
    if not mentor_id or not date or not time:
        return Response({'success': False, 'error': 'Mentor ID, date, and time are required.'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        mentor = User.objects.get(id=mentor_id, role='MENTOR')
    except User.DoesNotExist:
        return Response({'success': False, 'error': 'Mentor not found.'}, 
                       status=status.HTTP_404_NOT_FOUND)
    
    session = MentorshipSession.objects.create(
        mentor=mentor,
        student=request.user,
        session_type=session_type,
        date=date,
        time=time,
        status='PENDING',
    )
    
    # Generate access code for booking
    access_code = secrets.token_hex(4).upper()
    Booking.objects.create(
        session=session,
        access_code=access_code,
        payment_status='UNPAID'
    )
    
    return Response({
        'success': True,
        'message': 'Session booked successfully.',
        'session_id': session.id,
        'access_code': access_code,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_list_api(request):
    bookings = Booking.objects.filter(session__student=request.user).select_related('session', 'session__mentor')
    data = [{
        'id': b.id,
        'session_id': b.session.id,
        'mentor': getattr(b.session.mentor, 'full_name', None) or b.session.mentor.email,
        'date': str(b.session.date),
        'time': str(b.session.time),
        'meeting_link': b.session.meeting_link,
        'status': b.session.status,
        'payment_status': b.payment_status,
        'access_code': b.access_code,
    } for b in bookings]
    return Response({'success': True, 'bookings': data})