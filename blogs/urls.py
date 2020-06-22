from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='blogs'
urlpatterns = [
    path('logout/',views.logout ,name='logout'),
    path('',views.home ,name='home'),
    path('profile/',views.profile ,name='profile'),
    path('new_blog/',views.newBlog ,name='newBlog'),
    path('my_blogs/',views.myBlogs ,name='myBlogs'),
    path('search/',views.search ,name='search'),
    path('search_community/',views.searchCommunity ,name='searchCommunity'),
    path('contact/',views.contact ,name='contact'),
    path('blog_post/<int:blog_pk>/delete',views.deleteBlog ,name='deleteBlog'),
    path('blog_post/<int:blog_pk>',views.blogPost ,name='blogPost'),
    path('blog_post/viewUser/<int:usr_id>',views.viewUser ,name='viewUser'),
    path('edit_profile/<int:user_id>',views.Editprofile ,name='Editprofile'),
    path('community_post/<int:community_id>',views.communityPosts ,name='communityPosts'),
    path('community_list/',views.communityList ,name='communityList'),
    path('community_create/',views.communityForm ,name='communityForm'),
    path('upvote/<int:blog_pk>',views.upVote,name='upVote'),
    path('downvote/<int:blog_pk>',views.downVote,name='downVote'),
    path('saved/<int:blog_pk>',views.saved,name='saved'),
    path('sort_upvote/<str:page>',views.sortUpvotes,name='sortUpvotes'),
    path('sort_downvote/<str:page>',views.sortDownvotes,name='sortDownvotes'),
    path('saved_blogs',views.savedBlogs,name='savedBlogs'),
    path('sort_new/<str:page>',views.sortNew,name='sortNew'),
    path('sort_old/<str:page>',views.sortOld,name='sortOld'),
    path('trending_today/<str:page>',views.trendingToday,name='trendingToday'),
    path('community_post_sort_upvotes/<int:community_id>',views.sortUpvotesComm ,name='sortUpvotesComm'),
    path('community_post_sort_downvotes/<int:community_id>',views.sortDownvotesComm ,name='sortDownvotesComm'),
    path('community_post_sort_new/<int:community_id>',views.sortNewComm ,name='sortNewComm'),
    path('community_post_sort_old/<int:community_id>',views.sortOldComm ,name='sortOldComm'),
    path('community_post_trending_today/<int:community_id>',views.trendingTodayComm ,name='trendingTodayComm'),
    path('delete_comment/<int:comment_pk>/<int:blog_pk>',views.deleteComment,name='deleteComment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



