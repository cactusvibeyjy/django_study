from django.http import JsonResponse
from django.shortcuts import render, redirect
from sympy import re
import urllib.parse
from django.db.models import Q
from myapp01.models import Board, comment
from django.http.response import JsonResponse,HttpResponse
import math

# Create your views here.
UPLOAD_DIR = 'C:\\djangoStudy\\upload\\'
#write_form
def write_form(request):
    return render(request, 'board/write.html')

from django.views.decorators.csrf import csrf_exempt
#insert
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


# #전체보기
# def list(request):
#     boardList = Board.objects.all()
#     context ={'boardList' : boardList}
#     return render(request, 'board/list.html', context)

#전체보기 + 검색
def list(request):
    page = request.GET.get('page', 1)
    word = request.GET.get('word', '')
    field =request.GET.get('filed', 'title')
    #페이징 1,2,3, [다음] -> [이전]4,5,6[다음]
    pageSize = 5 #한 화면에 나타날 게시글 수
    blockPage =3 #보이는 페이지의 수 1,2,3 
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
    #페이징 1,2,3, [다음] -> [이전]4,5,6[다음]
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

    #검색내용
    if field == 'all':
       boardList =  Board.objects.filter(Q(writer__contains=word)|Q(title__contains=word)|Q(content__contains=word)).order_by('-idx')[start:start+pageSize]
    elif field =='writer':
        boardList =  Board.objects.filter(Q(writer__contains=word)).order_by('-idx')[start:start+pageSize]
    elif field =='title':
        boardList =  Board.objects.filter(Q(title__contains=word)).order_by('-idx')[start:start+pageSize]
    elif field == 'content':
        boardList =  Board.objects.filter(Q(content__contains=word)).order_by('-idx')[start:start+pageSize]
    else:
        boardList =  Board.objects.all().order_by('-idx')[start:start+pageSize]
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






#detail_idx 클릭시 detail.html로 이동 => 상세보기
def detail_idx(request):
    id = request.GET['idx']
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    commentList = comment.objects.filter(board_idx=id).order_by('-idx')
    return render(request, 'board/detail.html',{'dto':dto, 'commentList': commentList} )

#상세보기 detail/숫자
def detail(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
    
    dto.hit_up()
    dto.save()
    commentList = comment.objects.filter(board_idx=board_idx).order_by('-idx')
    return render(request, 'board/detail.html',{'dto':dto, 'commentList': commentList} )
    
    
    # return render(request, 'board/detail.html', {'dto':dto})

#수정폼으로 이동
def update_form(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
    return render(request, 'board/update.html',{'dto':dto})

#수정하기
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update(request):
    id=request.POST['idx']
    dto = Board.objects.get(idx=id)
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
def delete(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
   
    dto.delete()
    return redirect('/list')

#다운로드 카운트
def download_count(request):
    id = request.GET['idx']
    print('id: ', id)

    dto = Board.objects.get(idx=id)
    dto.down_up()
    dto.save()
    count = dto.down
    print('count: ', count)
    return JsonResponse({'idx': id, 'count': count})


#다운로드
def download(request):
    id=request.GET['idx']
    dto = Board.objects.get(idx=id)
    path = UPLOAD_DIR+dto.filename
    filename = urllib.parse.quote(dto.filename)
    print('filename: ', filename)
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment;filename*=UTF-8''{0}".format(filename)
    return response

#comment_insert
@csrf_exempt
def comment_insert(request):
    id=request.POST['idx']
    dto= comment(board_idx= id,
                writer= 'aa',
                content=request.POST['content'])
    dto.save()
    #return render(request, 'board/detail.html',{'dto':dto})
    return redirect("/detail_idx?idx="+id)