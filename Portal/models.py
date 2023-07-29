from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from django.db.models import Q








class Author(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    author_rank = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Справочник Авторов'
        verbose_name_plural = 'Справочник Авторов'
        ordering = ['author_rank']

    def update_rating(self):

        postsX = Post.objects.filter(author_ID_FK=self.user.pk)
        try:
            p_rating = postsX.aggregate(p_rating=Sum('post_rank'))['p_rating'] * 3
        except TypeError:
            p_rating = 0

        commentsX=Comments.objects.filter(user_id=self.user.pk)
        try:
            c_rating = commentsX.aggregate(comment_rank=Sum('comment_rank'))['comment_rank']
        except TypeError:
            c_rating = 0

        P_C = Comments.objects.filter(Q(user_id=self.user.pk), Q(post_ID_FK__in=postsX))
        try:
            p_c_rating = P_C.aggregate(comment_rank=Sum('comment_rank'))['comment_rank']
            if p_c_rating==None:
                p_c_rating=0

        except TypeError:
            p_c_rating = 0


        self.author_rank = p_rating + c_rating + p_c_rating
        self.save()



class Category(models.Model):
    categoryID = models.BigAutoField(primary_key=True, verbose_name='ID')
    categoryTitle = models.CharField(max_length=250, unique=True, db_index=True, verbose_name='Категория')

    def __str__(self):
        return self.categoryTitle

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Справочник категорий'
        ordering = ['categoryID']


article='ART'
news='NEWS'
POST_TYPE=[
    (article,'Статья'),
    (news,'Новость')
]


class Post(models.Model):
    post_ID = models.BigAutoField(primary_key=True, verbose_name='ID')
    author_ID_FK = models.ForeignKey('Author', db_column='author_ID_FK', to_field='user_id',
                                        on_delete=models.PROTECT,db_constraint=True)
    post_type=models.CharField(max_length=4, choices=POST_TYPE,default=article)
    date_and_time_created = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    category_ID_FK=models.ManyToManyField(Category,through='PostCategory', verbose_name='связь многие ко многим')
    post_title=models.CharField(max_length=150, unique=True, verbose_name='Заголовок')
    post_content = models.CharField(max_length=250, unique=True, verbose_name='Текст')
    post_rank=models.IntegerField(default=0, verbose_name='Рейтинг ')

    def __str__(self):
        return f'{self.post_ID}'

    def like(self):
        self.post_rank += 1
        self.save()

    def dislike(self):
        if self.post_rank > 0:
            self.post_rank -= 1
            self.save()

    def preview(self):
        return self.post_content[:124]+'...'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'






class PostCategory(models.Model):
    post_ID_FK = models.ForeignKey(Post, on_delete = models.CASCADE)
    category_ID_FK = models.ForeignKey(Category, on_delete = models.CASCADE)



class Comments(models.Model):
    commend_ID = models.BigAutoField(primary_key=True, verbose_name='ID')
    post_ID_FK = models.ForeignKey('Post', db_column='post_ID_FK', to_field='post_ID',
                                        on_delete=models.PROTECT,db_constraint=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text=models.CharField(max_length=250, unique=True, verbose_name='Текст')
    comment_created = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')
    comment_rank=models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.commend_ID}'
    def like(self):
                self.comment_rank += 1
                self.save()



    def dislike(self):
        if self.comment_rank>0 :
           self.comment_rank-=1
           self.save()




    class Meta:

        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'


