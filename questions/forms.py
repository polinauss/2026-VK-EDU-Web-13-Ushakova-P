from django import forms
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'python, django, javascript'})
    )

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

    def clean_tags(self):
        tag_str = self.cleaned_data.get('tags', '')
        tags = [t.strip().lower() for t in tag_str.split(',') if t.strip()]
        if len(tags) > 5:
            raise forms.ValidationError('Maximum 5 tags allowed.')
        for tag_name in tags:
            if not tag_name.replace('-', '').isalnum():
                raise forms.ValidationError(f'Invalid tag: "{tag_name}".')
        return tags

    def save_tags(self, question):
        tag_names = self.cleaned_data.get('tags', [])
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        question.tags.set(tags)

    def save(self, commit=True):
        question = super().save(commit=False)
        if commit:
            question.save()
            self.save_tags(question)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your answer here...'})
        }
