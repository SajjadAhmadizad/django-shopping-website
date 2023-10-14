function changeList(changeTo) {
    if (changeTo == 'normal' && !location.href.includes('list-display=normal')) {
        $("#product-display").val(changeTo);
        $("#change-url").submit();
    } else if (changeTo == 'list' && !location.href.includes('list-display=list')) {
        $("#product-display").val(changeTo);
        $("#change-url").submit();
    }
}

function fillPage(pageNumber) {
    $('#page').val(pageNumber);
    $("#change-url").submit();
}

function paginateBy() {
    var number = parseInt(document.getElementById('current').innerHTML);
    if (number === 2 || number === 12 || number === 24 || number === 48) {
        $("#paginate_by").val(number);
        $("#page").val(1);
        $("#change-url").submit();
    }
}

$("#paginate-by-form").on('change', paginateBy);

function func() {
    var selected = [];
    $('#form-check input:checked').each(function () {
        selected.push($(this).val());
        $("#brand_value").val(selected.join(','));
        $("#page").val(1);
        $("#change-url").submit();
    });
    if (selected.length == 0) {
        $("#brand_value").val('');
        $("#page").val(1);
        $("#change-url").submit();
    }
}

$(".widget-desc").on('change', func)

function orderBy(event) {
    var orderby = document.getElementById('order-by').innerHTML;
    // console.log(orderby);
    $('#order_by').val(orderby);
    // # it is not important but:
    $('#page').val(1);
    $("#change-url").submit();
}

$('#order-by-b').on('change', orderBy);


function filterPrice() {
    var range = document.getElementById('range-price').innerHTML.split('-');
    // console.log(range);
    $("#max_price").val(parseInt(range[1]));
    $("#min_price").val(parseInt(range[0]));
    $('#page').val(1);
    $("#change-url").submit();
}

$("#filter-price").on('click', filterPrice);


function setAsLargeImage(src) {
    // console.log(src);
    $("#lrg-img").attr('src', src);
    $(".mfp-img").attr('src', src);
    $("src").attr('src', src);

}

var productCommentForm = document.getElementById('product-comment-form');
if (productCommentForm) {
    productCommentForm.addEventListener('submit', function (event) {
        event.preventDefault();
        var form = $(document.forms['product-comment-form']).serialize();
        $.post('', form, function (response) {
            if (response.status === 'success') {
                var parent = document.getElementById('parent').value;
                if (parent === '') {
                    document.getElementById('scroll-to-here').scrollIntoView({behavior: 'smooth'});
                } else {
                    document.getElementById(parent).scrollIntoView({behavior: 'smooth'});
                }
                $("#comments-area").html(response.body);
            } else if (response.status === 'error') {
                console.log(response.message);
            }
        })
    })

}

function submitRegisterForm(event) {
    event.preventDefault();
    myFunction();
}

function myFunction() {
    var form = $(document.forms['register-form']).serialize();

    $.post('', form, function (response) {
        // $("#sign-up-form").html(response.body);
        $("#register-form").html(response.body);
        if (response.status == 'success') {
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            })

            Toast.fire({
                icon: 'success',
                title: response.message
            })
        }
        document.getElementById("register-form").addEventListener("submit", submitRegisterForm);
    })
}

var registerForm = document.getElementById("register-form");
if (registerForm) {
    registerForm.addEventListener("submit", submitRegisterForm);
}


function submitLoginForm(event) {
    event.preventDefault();
    var form = $(document.forms['login-form']).serialize();
    $.post('/user/login-form-submit/', form, function (response) {
        $("#login-form").html(response.body);
        document.getElementById('login-form').addEventListener('submit', submitLoginForm);
        if (response.status === 'success') {
            location.href = response.redirectTo;
        }
    })
}

var signINForm = document.getElementById('login-form');
if (signINForm) {
    signINForm.addEventListener('submit', submitLoginForm);
}


// stackowerflow's help:
// https://stackoverflow.com/questions/26243029/javascript-addeventlistener-not-working-more-than-once/26243095#26243095


function addProductToOrder(productId) {
    var count = document.getElementById('qty');
    if (count === null) {
        count = 1;
    } else {
        count = count.value;
    }
    $.get('/order/add-product-to-order?product_id=' + productId + '&count=' + count).then(res => {
        if (res.status === 'not auth') {
            Swal.fire({
                position: 'top-end',
                icon: res.icon,
                title: res.message,
                showConfirmButton: true,
                confirmButtonText: res.button,
                timer: 2500
            }).then((result) => {
                if (result.isConfirmed) {
                    location.href = res.redirectTo
                }
            })
        } else {
            Swal.fire({
                position: 'top-end',
                icon: res.icon,
                title: res.message,
                showConfirmButton: false,
                timer: 2500
            })
            try {
                if (res.current_count > 0) {
                    var deleteBotton = document.getElementById('delete-order-button')
                    document.getElementById('count-in-order-p').innerHTML = 'این محصول به تعداد ' + res.current_count + ' عدد در سبد خرید شما موجود است';
                    deleteBotton.hidden = false;
                    // deleteBotton.onclick = function (){
                    //     deleteOrderItemCount(res.order_item_id)
                    // }
                    deleteBotton.addEventListener('click', function () {
                        deleteOrderItemCount(res.order_item_id);
                    })
                }
            } catch {
                null
            }
        }
    })
}


function addOrderItemCount(orderItemsId, x) {
    if (x === 'increase' || x === 'decrease') {
        $.get('change-product-count', {
            orderItemsId: orderItemsId,
            todo: x
        }).then(res => {
            if (res.status === 'success') {
                $('#order-items').html(res.body);
            }
        })
    }
}


function deleteOrderItemCount(orderItemsId) {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: 'توجه!',
        text: "محصول موردنظر از سبد خرید حذف شود؟",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'خیر',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('/order/delete-product', {
                orderItemsId: orderItemsId,
            }).then(res => {
                if (res.status === 'success') {
                    try {
                        document.getElementById('order-items').innerHTML = res.body;
                    } catch {
                        document.getElementById('count-in-order-p').innerHTML = '';
                        document.getElementById('delete-order-button').hidden = true;
                    }
                    swalWithBootstrapButtons.fire(
                        res.m1,
                        res.m2,
                        res.status,
                    )
                } else if (res.status === 'error') {
                    swalWithBootstrapButtons.fire(
                        res.m1,
                        res.m2,
                        res.status
                    )
                }
            })

        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            swalWithBootstrapButtons.fire(
                'لغو شد',
                'لفو شد',
                'error'
            )
        }
    })
}


function replyComment(commentId, replyTo = null) {
    var parent = document.getElementById('parent');
    parent.value = commentId;
    var replyArea = document.getElementById('reply-area');
    replyArea.innerHTML = 'درحال پاسخ به ' + replyTo;
    replyArea.addEventListener('click', function (res) {
        parent.value = null;
        replyArea.innerHTML = 'نظر خود را بنویسید:'
    })
    document.getElementById('top-of-comment-form').scrollIntoView({behavior: 'smooth'});
}


function likeProductComment(commentId) {
    var likeForm = $(document.forms['like-form-' + commentId]).serialize();
    $.post('', likeForm, function (res) {
        document.getElementById('like-count-' + res.comment_id).innerHTML = res.count;
    })
}


function deleteProductComment(commentId) {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: 'توجه!',
        text: "کامنت مورد نظر حذف شود؟",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'بله',
        cancelButtonText: 'خیر',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            $.get('/product-list/delete-product-comment/', {
                commentId: commentId
            }).then(res => {
                if (res.status === 'success') {
                    $("#comments-area").html(res.body);
                    swalWithBootstrapButtons.fire(
                        'حذف شد',
                        res.message,
                        res.status,
                    )
                } else if (res.status === 'error') {
                    swalWithBootstrapButtons.fire(
                        'ارور',
                        res.message,
                        res.status
                    )
                }
            })

        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            swalWithBootstrapButtons.fire(
                'لغو شد',
                'لفو شد',
                'error'
            )
        }
    })
}


var contactForm = document.getElementById('contact-us-form');
if (contactForm) {
    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();
        var form = $(document.forms['contact-us-form']).serialize();
        $.post('', form, function (res) {
            if (res.status === 'success') {
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }
                })

                Toast.fire({
                    icon: 'success',
                    title: res.message
                })
            } else {
                $('#contact-us-form').html(res.body);
            }
        })
    })
}


function forgotPasswordLoggedInUser() {
    $.get('/user/forgot-password-logged-in-user', function (res) {
        if (res.status === 'success') {
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 6000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            })
            Toast.fire({
                icon: 'success',
                title: 'ایمیل بازیابی کلمه عبور با موفقیت ارسال شد'
            })
        } else if (res.status === 'time_error') {
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 6000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            })
            Toast.fire({
                icon: 'error',
                title: 'از آخرین زمان ارسال ایمیل بازیابی کلمه عبور کمتر از 5 دقیقه گذشته است.لطفا منتظر بمانید...'
            })
        }
    })
}


var forgotPasswordForm_ = document.getElementById('forgot-password-form');
if (forgotPasswordForm_) {
    forgotPasswordForm_.addEventListener('submit', forgotPasswordForm)
}

function forgotPasswordForm(event) {
    event.preventDefault();
    var form = $(document.forms['forgot-password-form']).serialize();
    $.post('', form, function (res) {
        if (document.getElementById('forgot-password-form')) {
            $("#forgot-password-form").html(res.body);
        }
        if (res.status === 'success') {
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            })
            Toast.fire({
                icon: 'success',
                title: res.message
            })
        } else if (res.status === 'time_error') {
            const Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 6000,
                timerProgressBar: true,
                didOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                }
            })
            Toast.fire({
                icon: 'error',
                title: 'از آخرین زمان ارسال ایمیل بازیابی کلمه عبور کمتر از 5 دقیقه گذشته است.لطفا منتظر بمانید...'
            })
        }
    })
}


var resetPasswordForm = document.getElementById('reset-password-form');
if (resetPasswordForm) {
    resetPasswordForm.addEventListener('submit', function (event) {
        event.preventDefault();
        var form = $(document.forms['reset-password-form']).serialize();
        $.post('', form, function (res) {
            $("#reset-password-form").html(res.body);
            if (res.status === 'success') {
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer);
                        toast.addEventListener('mouseleave', Swal.resumeTimer);
                    }
                });
                Toast.fire({
                    icon: 'success',
                    title: res.message
                });
            }
        });
    });
}


var searchBar = document.getElementById('product-search');
if (searchBar) {
    var before = '';
    searchBar.addEventListener('input', searchProduct);
}

function searchProduct() {
    var text = searchBar.value.trim();

    if (text === '') {
        null;
    } else if (before !== text) {
        var form = $(document.forms['search-bar-form']).serialize();
        $.post('/product-list/search-product-component/', form, function (res) {
            if (res.status === 'success') {
                $('#suggested-products').html(res.body);
                searchBar.addEventListener('input', searchProduct);
            }
        })
        before = text;
    }
}

var searchProductView = document.getElementById('search-bar-form');
if (searchProductView) {
    searchProductView.addEventListener('submit', searchProductViewFunction);
}

function searchProductViewFunction(event) {
    event.preventDefault();
    var text = document.getElementById('product-search').value;
    text = text.trim();
    if (text !== '') {
        location.href = '/product-list?q=' + text;
    }
}

function closeSearch() {
    var suggestedProducts = document.getElementById('suggested-products');
    if (suggestedProducts.hidden === true) {
        suggestedProducts.hidden = false;
    } else {
        suggestedProducts.hidden = true;
    }
}


function soon(x) {
    if (x === 'checkOut') {
        const swalWithBootstrapButtons = Swal.mixin({
            customClass: {
                confirmButton: 'btn btn-success',
                cancelButton: 'btn btn-danger'
            },
            buttonsStyling: false
        })

        swalWithBootstrapButtons.fire({
            title: 'ارور!',
            text: "درگاه پرداخت کامل نیست!",
            icon: 'error',
        })
    }

}