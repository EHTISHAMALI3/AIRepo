<div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 p-6">
  <div class="bg-white shadow-2xl rounded-3xl p-8 w-full max-w-lg transition-transform hover:scale-[1.02] duration-300">
    <h1 class="text-3xl font-extrabold text-gray-800 text-center mb-6">
      🧠 Toxic Comment Detector
    </h1>

    <!-- Textarea -->
    <textarea
      [(ngModel)]="commentText"
      placeholder="Type your comment here..."
      class="w-full border border-gray-300 rounded-2xl p-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
      rows="5"
    ></textarea>

    <!-- Analyze Button -->
    <button
      (click)="analyzeComment()"
      [disabled]="loading || !commentText.trim()"
      class="mt-4 w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-2xl font-semibold hover:opacity-90 disabled:opacity-50 transition-all duration-300"
    >
      {{ loading ? '🔍 Analyzing...' : '🚀 Analyze Comment' }}
    </button>

    <!-- Prediction Result -->
    <div *ngIf="prediction" class="mt-8 text-center animate-fadeIn">
      <!-- Emoji instead of text -->
      <div class="text-6xl mb-4">
        {{ prediction.is_toxic ? '😡' : '😇' }}
      </div>

      <!-- Confidence Progress Bar -->
      <div class="w-full bg-gray-200 rounded-full h-6 overflow-hidden shadow-inner">
        <div
          class="h-6 transition-all duration-1000"
          [ngClass]="{
            'bg-red-500': prediction.is_toxic,
            'bg-green-500': !prediction.is_toxic
          }"
          [style.width.%]="prediction.confidence * 100"
        ></div>
      </div>

      <div class="mt-2 text-gray-700 font-semibold">
        {{ (prediction.confidence * 100) | number:'1.0-1' }}%
      </div>
    </div>
  </div>
</div>



















commentText = '';
  prediction: any = null;
  loading = false;

  constructor(private http: HttpClient) {}

  analyzeComment() {
    if (!this.commentText.trim()) return;

    this.loading = true;
    this.prediction = null;

    this.http
      .post('http://127.0.0.1:8000/predict', { text: this.commentText })
      .subscribe({
        next: (res: any) => {
          this.prediction = res;
          this.loading = false;
        },
        error: (err) => {
          console.error('Error analyzing comment:', err);
          this.loading = false;
        },
      });
  }
