from django.shortcuts import render,  get_object_or_404, reverse
from django.views import generic
from django.contrib import messages 
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import CommentForm, PostForm
from slugify import slugify




# Create your views here.


class PostList(generic.ListView):
    
    queryset = Post.objects.filter(status=1)
    template_name = "blog/index.html"
    paginate_by = 6
    
def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    if request.method == "POST":
       comment_form = CommentForm(data=request.POST)
       if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.author = request.user
          comment.post = post
          comment.save()
          messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting approval'
    )
        
    comment_form = CommentForm()


    return render(
    request,
    "blog/post_detail.html",
    {
        "post": post,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    },
    )
    
def comment_edit(request, slug, comment_id):
        """
        view to edit comments
        """
        if request.method == "POST":

          queryset = Post.objects.filter(status=1)
          post = get_object_or_404(queryset, slug=slug)
          comment = get_object_or_404(Comment, pk=comment_id)
          comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    
def comment_delete(request, slug, comment_id):
        """
        view to delete comment
        """
        queryset = Post.objects.filter(status=1)
        comment = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author == request.user:
            comment.delete()
            messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
        else:
            messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    
def post(request):
        post_form = PostForm()
        if request.method == "POST":
           post_form = PostForm(data=request.POST)
           if post_form.is_valid():
              post = post_form.save(commit=False)
              post.author = request.user
              post.slug = slugify(post.title)
              post.status = 1
              post_form.save()
              messages.add_message(request, messages.SUCCESS, "Post created successfully ")
   # addpost = AddPost.objects.all().order_by('-updated_on').first()
    

        return render(
        request,
        "blog/post.html",
        {
           # "addpost": addpost,
            "post_form": post_form
        },
    )
        
def post_edit(request, slug, post_id):
        """
        view to edit post
        """
        if request.method == "POST":

          queryset = Post.objects.filter(status=1)
          post = get_object_or_404(queryset, slug=slug)
          post = get_object_or_404(Comment, pk=post_id)
          post_form = PostForm(data=request.POST, instance=post)

        if post_form.is_valid() and post.author == request.user:
            post = post_form.save(commit=False)
            post.post = post
            post.approved = False
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Post Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating Post!')

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    
def post_delete(request, slug, post_id):
        """
        view to delete post
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        post = get_object_or_404(Post, pk=post_id)

        if post.author == request.user:
            post.delete()
            messages.add_message(request, messages.SUCCESS, 'Post deleted!')
        else:
            messages.add_message(request, messages.ERROR, 'You can only delete your own Post!')

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    