from django import forms
from .models import Question, Answer, Tag

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        label='Tags',
        required=False,
        help_text='Separate tags with commas. Maximum 5 tags.',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'python, django, javascript'})
    )

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "What's your question? Be specific."}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Describe your problem in detail...'}),
        }

    def clean_tags(self):
        tag_str = self.cleaned_data.get('tags', '')
        tags = [t.strip().lower() for t in tag_str.split(',') if t.strip()]
        if len(tags) > 5:
            raise forms.ValidationError('Maximum 5 tags allowed.')
        for tag_name in tags:
            # Разрешены только буквы, цифры и дефисы
            if not tag_name.replace('-', '').isalnum():
                raise forms.ValidationError(f'Invalid tag: "{tag_name}". Use only letters, numbers, and hyphens.')
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
        # author устанавливается во view
        if commit:
            question.save()
            self.save_tags(question)
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter your answer here.'})
        }
