from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from myapp02.models import Board
from django.db.models import Q
import math
from django.http import JsonResponse
from django.http.response import JsonResponse,HttpResponse
import urllib.parse
from django.core.paginator import Paginator

# Create your views here.
UPLOAD_DIR = 'C:\\djangoStudy\\upload\\'
def base(request):
    return render(request, 'base.html')

def write_form(request):
    return render(request, 'board/insert.html')

@csrf_exempt
def insert(request):
    fname = ''
    fsize = 0

    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size
        fp = open('%s%s' %(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    dto = Board(writer=request.POST['writer'],
        title = request.POST['title'],
        content = request.POST['content'],
        filename=fname,
        filesize=fsize
    )
    dto.save()
    return redirect('/list/')

def list(request):
    page = request.GET.get('page', 1)
    word = request.GET.get('word', '')
    field = request.GET.get('field', 'title')
    # context={'boardList': boardList}
    # boardCount =  Board.objects.all().count()
    if field == 'all':
        boardCount =  Board.objects.filter(Q(writer__contains=word)|Q(title__contains=word)|Q(content__contains=word)).count()
    elif field =='writer':
        boardCount =  Board.objects.filter(Q(writer__contains=word)).count()
    elif field =='title':
        boardCount =  Board.objects.filter(Q(title__contains=word)).count()
    elif field == 'content':
        boardCount =  Board.objects.filter(Q(content__contains=word)).count()
    else:
        boardCount =  Board.objects.all().count()
    pageSize = 5 #한 화면에 나타날 게시글 수
    blockPage = 3 #보이는 페이지의 수 1,2,3 
    currentPage= int(page)
    start = (currentPage-1)* pageSize
    
    #게시글의 전체 페이지 수 
    totPage= math.ceil(boardCount/pageSize)
    startPage = math.floor((currentPage-1) / blockPage)*blockPage +1
    endPage = startPage + blockPage -1
    if endPage > totPage :
        endPage = totPage
    # boardList=Board.objects.all().order_by("-id")[start:start+pageSize]
    if field == 'all':
       boardList =  Board.objects.filter(Q(writer__contains=word)|Q(title__contains=word)|Q(content__contains=word)).order_by('-id')[start:start+pageSize]
    elif field =='writer':
        boardList =  Board.objects.filter(Q(writer__contains=word)).order_by('-id')[start:start+pageSize]
    elif field =='title':
        boardList =  Board.objects.filter(Q(title__contains=word)).order_by('-id')[start:start+pageSize]
    elif field == 'content':
        boardList =  Board.objects.filter(Q(content__contains=word)).order_by('-id')[start:start+pageSize]
    else:
        boardList =  Board.objects.all().order_by('-id')[start:start+pageSize]
    context ={'boardList' : boardList,
              'startPage' : startPage,
              'blockPage' : blockPage,
              'endPage' : endPage,
              'totPage' : totPage,
              'boardCount' : boardCount,
              'currentPage' : currentPage,
              'field' : field,
              'word' : word,
              'range' : range(startPage, endPage+1)}
    return render(request, 'board/list.html', context)

    #다운로드 카운트
def download_count(request):
    id = request.GET['id']
    print('id: ', id)

    dto = Board.objects.get(id=id)
    dto.down_up()
    dto.save()
    count = dto.down
    print('count: ', count)
    return JsonResponse({'id': id, 'count': count})


#다운로드
def download(request):
    id=request.GET['id']
    dto = Board.objects.get(id=id)
    path = UPLOAD_DIR+dto.filename
    filename = urllib.parse.quote(dto.filename)
    print('filename: ', filename)
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment;filename*=UTF-8''{0}".format(filename)
    return response


#list_page
def list_page(request):
    page = request.GET.get('page', '1')
    word = request.GET.get('word', '')
    boardCount = Board.objects.filter(Q(writer__contains=word)|Q(title__contains=word)|Q(content__contains=word)).count()
    boardList = Board.objects.filter(Q(writer__contains=word)|Q(title__contains=word)|Q(content__contains=word)).order_by('-id')
    pageSize= 5
    #페이징 처리
    paginator = Paginator(boardList, pageSize)
    page_objc = paginator.get_page(page)
    print('boardCount: ', boardCount)
    context ={'page_list': page_objc,
              'page' : page,
              'word' : word,
              'boardCount': boardCount}
    return render(request, 'board/list_page.html', context)

def detail_id(request):
    id = request.GET['id']
    dto = Board.objects.get(id=id)
    dto.hit_up()
    dto.save()
    # commentList = comment.objects.filter(board_idx=id).order_by('-idx')
    return render(request, 'board/detail.html',{'dto':dto} )

def detail(request, board_id):
    dto = Board.objects.get(id=board_id)
    
    dto.hit_up()
    dto.save()
    # commentList = comment.objects.filter(board_idx=board_idx).order_by('-idx')
    return render(request, 'board/detail.html',{'dto':dto})   

#수정폼으로 이동
def update_form(request, board_id):
    dto = Board.objects.get(id=board_id)
    return render(request, 'board/update.html',{'dto':dto})

#수정하기
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update(request):
    id=request.POST['id']
    dto = Board.objects.get(id=id)
    fname = dto.filename
    fsize = dto.filesize

    if 'file' in request.FILES:
        file = request.FILES['file']
        fname = file.name
        fsize = file.size
        fp = open('%s%s' %(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
            fp.close()
    update_dto = Board(id,
        writer=request.POST['writer'],
        title = request.POST['title'],
        content = request.POST['content'],
        filename=fname,
        filesize=fsize
    )
    update_dto.save()
    return redirect('/list')

#삭제하기
def delete(request, board_id):
    dto = Board.objects.get(id=board_id)
   
    dto.delete()
    return redirect('/list')